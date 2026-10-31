import pandas as pd
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def residuos_y_ajustados(modelo): return modelo.resid, modelo.fittedvalues

def prueba_shapiro(residuos, alfa=0.05):
    stat, p = stats.shapiro(residuos)
    return stat, p, "Se cumple (Normal)" if p >= alfa else "No se cumple (No normal)"

def prueba_levene(df, col_trat, col_resp, alfa=0.05):
    grupos = [g[col_resp].values for _, g in df.groupby(col_trat)]
    stat, p = stats.levene(*grupos, center="median")
    return stat, p, "Se cumple (Homogéneas)" if p >= alfa else "No se cumple (Heterogéneas)"

def grafico_residuos_vs_ajustados(ajustados, residuos):
    fig = px.scatter(x=ajustados, y=residuos, labels={'x': 'Valores Ajustados', 'y': 'Residuos'}, title='Homocedasticidad')
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    return fig

def grafico_qq(residuos):
    qq = stats.probplot(residuos, dist="norm")
    fig = px.scatter(x=qq[0][0], y=qq[0][1], labels={'x': 'Teóricos', 'y': 'Residuos'}, title='Normalidad (Q-Q)')
    fig.add_trace(go.Scatter(x=[min(qq[0][0]), max(qq[0][0])], y=[qq[1][0]*min(qq[0][0])+qq[1][1], qq[1][0]*max(qq[0][0])+qq[1][1]], mode='lines', name='Referencia', line=dict(color='red', dash='dash')))
    return fig