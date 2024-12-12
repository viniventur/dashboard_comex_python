import pandas as pd
import streamlit as st
import requests
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

@st.cache_data
def get_comexstat_uf(uf):
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
                "values": [uf]
            }
        ],
        "details": ["state", "chapter", 'country'],
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
            if not df.empty:
                df['Fluxo'] = flow  # Marca o fluxo correspondente
                # Concatena ao DataFrame final
                df_comexstat = pd.concat([df_comexstat, df], axis=0, ignore_index=True)
        else:
            return f"Erro na requisição ao COMEXSTAT: {response.status_code}"

    # Verifica se o DataFrame final está vazio
    if df_comexstat.empty:
        return f"Nenhum dado foi retornado pelo COMEXSTAT. Verifique os parâmetros ou tente novamente mais tarde. Status: {response.status_code}"

    # Retorna o DataFrame final
    return df_comexstat

@st.cache_data
def metadados_uf_comexstat():

    url = "https://api-comexstat.mdic.gov.br/tables/uf"

    response = requests.get(url, verify=False)

    df_uf = pd.json_normalize(response.json()['data'])
    
    return df_uf
