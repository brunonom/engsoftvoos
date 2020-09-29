import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from getDataframe import getDataframe

df = getDataframe()

empresaSum = df.groupby(["Empresa"]).sum().reset_index()

app = dash.Dash()

app.layout = html.Div([
    html.H1(children="Dashboard de Análise: Histórico de Voos ANAC"),
    dcc.Graph(
        id="empresa-partida-delay-bar",
        figure=px.bar(
            empresaSum,
            title="Atraso da Partida total em minutos por Empresa",
            x="Empresa",
            y="Partida Delay",
        )
    ),
    dcc.Graph(
        id="empresa-chegada-delay-bar",
        figure=px.bar(
            empresaSum,
            title="Atraso da Chegada total em minutos por Empresa",
            x="Empresa",
            y="Chegada Delay",
        )
    )
])

app.run_server(debug=True)
