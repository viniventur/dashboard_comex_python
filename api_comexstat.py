import pandas as pd
import requests
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')


def get_comexstat():


    # Obtém o ano e mês atuais
    data_atual = datetime.now()
    ano_atual = data_atual.year
    mes_atual = data_atual.month

    # Constrói o período atual no formato "YYYY-MM"
    periodo_atual = f"{ano_atual}-{str(mes_atual).zfill(2)}"
        
    # URL e configurações gerais
    url = "https://api-comexstat.mdic.gov.br/general"
    payload_template = {
        "monthDetail": True,
        "period": {
            "from": "2020-01",
            "to": periodo_atual
        },
            "filters": [
        {
            "filter": "state",
            "values": [27]
        }
    ],
        "details": ["state", "chapter"],
        "metrics": ["metricFOB", "metricKG"]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Lista de fluxos a serem consultados
    flows = ["import", "export"]

    # DataFrame para consolidar os resultados
    df_comexstat = pd.DataFrame()

    # Loop pelos fluxos
    for flow in flows:
        payload = payload_template.copy()
        payload["flow"] = flow  # Adiciona o fluxo atual ao payload
        
        response = requests.post(url, json=payload, headers=headers, verify=False)
        
        if response.status_code == 200:
            # Normaliza os dados recebidos em formato JSON e adiciona a coluna 'flow'
            df = pd.json_normalize(response.json()['data']['list'])
            df['flow'] = flow  # Marca o fluxo correspondente
            # Concatena ao DataFrame final
            df_comexstat = pd.concat([df_comexstat, df], axis=0, ignore_index=True)
        else:
            print(f"Erro na requisição para o fluxo '{flow}': {response.status_code}")

    # Exibir o DataFrame final
    return df_comexstat
