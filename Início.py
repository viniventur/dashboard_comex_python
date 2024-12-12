import streamlit as st
import requests
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from api_comexstat import *
from SBC_AL import *

st.set_page_config(layout="wide")


#with st.container():
st.write('''
            # Dashboard de Comércio Exterior de Alagoas
            ''')

with st.spinner('Aguardando COMEXSTAT...'):

    df_comexstat = get_comexstat_uf(27) # carregamento comexstat

    # tratamento
    
    df_comexstat.dropna(inplace=True)
    df_comexstat['Período'] = pd.to_datetime(df_comexstat['year'].astype(str) + '-' + df_comexstat['monthNumber'].astype(str))
    #df_comexstat = df_comexstat.set_index("Período")
    df_comexstat = df_comexstat.drop(['year', 'monthNumber'], axis=1)
    df_comexstat['metricFOB'] = df_comexstat['metricFOB'].astype(float)
    #df_comexstat.rename(columns={'year': 'Ano', 'monthNumber': 'Mês'}, inplace=True)

    st.write(df_comexstat)
    st.write(metadados_uf_comexstat())

    st.plotly_chart(fig_sbc)

st.header("Pré-tratamento")