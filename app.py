import streamlit as st
import requests
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from api_comexstat import get_comexstat

st.set_page_config(layout="wide")

def main():

    st.title('Olá! Bem vindo ao Dashboard de comércio exterior de Alagoas')

    with st.spinner('Carregando...'):

        df_comexstat = get_comexstat()
        
        st.write(df_comexstat)

main()