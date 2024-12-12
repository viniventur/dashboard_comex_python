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
            # SBC
            ''')

with st.spinner('Aguardando COMEXSTAT...'):

    st.plotly_chart(fig_sbc)
