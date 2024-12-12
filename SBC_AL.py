import pandas as pd
import requests
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')
from api_comexstat import *
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_comexstat_API = get_comexstat_uf(27) # alagoas
df_comexstat = df_comexstat_API.copy()

df_comexstat['Período'] = pd.to_datetime(df_comexstat['year'].astype(str) + '-' + df_comexstat['monthNumber'].astype(str))
df_comexstat[['metricFOB', 'metricKG']] = df_comexstat[['metricFOB', 'metricKG']].astype(float)

df_balanca = df_comexstat[['Período', 'Fluxo', 'metricFOB']]

df_import = df_balanca.loc[df_balanca.Fluxo == 'import'].drop(columns='Fluxo')
df_export = df_balanca.loc[df_balanca.Fluxo == 'export'].drop(columns='Fluxo')
df_import = df_import.groupby(['Período'], as_index=True).sum()
df_export = df_export.groupby(['Período'], as_index=True).sum()

# DF definitivo da SBC
df_import = df_import.rename(columns={'metricFOB': 'import'})
df_export = df_export.rename(columns={'metricFOB': 'export'})
df_sbc = pd.merge(df_import, df_export, on='Período')
df_sbc['SBC'] = df_sbc['export'] - df_sbc['import']

# Criando a figura com eixo Y secundário
fig_sbc = make_subplots(specs=[[{"secondary_y": True}]])

# Adicionando os traços
fig_sbc.add_trace(go.Scatter(x=df_sbc.index, y=df_sbc['import'],
                         name='Importação - USD$ (FOB)',
                         mode='lines',
                         line=dict(width=2, color='blue')),
              secondary_y=False)

fig_sbc.add_trace(go.Scatter(x=df_sbc.index, y=df_sbc['export'],
                         name='Exportação - USD$ (FOB)',
                         mode='lines+markers',
                         marker=dict(size=5, color='red'),
                         line=dict(width=2, color='red')),
              secondary_y=False)

fig_sbc.add_trace(go.Bar(x=df_sbc.index, y=df_sbc['SBC'],
                     name='Saldo da Balança Comercial',
                     marker_color='green', opacity=0.4),
              secondary_y=True)

# Adicionando linha horizontal no eixo Y secundário
fig_sbc.add_shape(
    type="line",
    x0=min(df_sbc.index),  # Ponto inicial no eixo X
    x1=max(df_sbc.index),  # Ponto final no eixo X
    y0=0,                  # Valor da linha no eixo Y secundário
    y1=0,                  # Valor da linha no eixo Y secundário
    xref="x",              # Referência ao eixo X
    yref="y2",             # Referência ao eixo Y secundário
    line=dict(color="black", width=2, dash="dash")  # Estilo da linha
)

# Atualizando layout
fig_sbc.update_layout(
    title='Saldo da Balança Comercial - Alagoas',
    title_font=dict(size=20),
    template='simple_white',
    height=700,
    width=1300,
    xaxis_title='Período',
    yaxis_title='USD$ (FOB)',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# Atualizando eixos
fig_sbc.update_yaxes(title_text="USD$ (FOB) - Importação e Exportação", secondary_y=False)
fig_sbc.update_yaxes(title_text="USD$ (FOB) - Saldo da Balança Comercial", secondary_y=True)

