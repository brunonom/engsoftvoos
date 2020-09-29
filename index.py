import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv("./2019/01.csv", encoding="latin-1", delimiter=";")
df = df.sample(3)
print(df.sample(3))

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(
        id="example-graph",
        figure=px.bar(df, x="ICAO Empresa Aérea", y="Número Voo", barmode="group")
    )
])

if __name__ == "__main__":
    app.run_server()
