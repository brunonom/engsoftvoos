import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from getDataframe import getDataframe
from dash.dependencies import Input, Output
from extractPlotData import extractPlotData

# df = getDataframe()

# empresaSum = df.groupby(["Empresa"]).sum().reset_index()
# print(empresaSum)
app = dash.Dash(__name__)

columns = ["Empresa",
			"Numero Voo",
			"Codigo DI",
			"Codigo Tipo Linha",
			"Origem",
			"Destino",
			"Partida Prevista",
			"Partida Real",
			"Chegada Prevista",
			"Chegada Real",
			"Situacao Voo",
			"Justificativa"]

app.layout = html.Div([
	html.H1("Dashboard de Análise: Histórico de Voos ANAC"),
	html.Div([
		# html.Label("X", htmlFor="choosex"),
		dcc.Dropdown(
			id="choosex", 
			options=[{"label": i, "value": i} for i in columns],
			value="Empresa"
			),
		# html.Label("Y", htmlFor="choosey"),
		dcc.Dropdown(
			id="choosey", 
			options=[{"label": i, "value": i} for i in columns],
			value="Empresa"
			),
		], style={'width': '48%', 'display': 'inline-block'}),

	html.Div([
		# html.Label("De", htmlFor="from"),
		dcc.Dropdown(
			id="fromyear",
			options=[{"label": i, "value": i} for i in range(2015, 2020)],
			value=2015
			),
		# html.Label("Até", htmlFor="to"),
		dcc.Dropdown(
			id="toyear",
			options=[{"label": i, "value": i} for i in range(2015, 2020)],
			value=2015
			),
		], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

	# html.Button("Plotar"),

	dcc.Graph(
		id="plot",
		figure=px.bar(
			extractPlotData("Empresa", "Empresa", 2015, 2015),
			title="Empresa x Empresa de 2015 até 2015",
			x="Empresa",
			y="Empresa",
		)
	),
])

@app.callback(
	Output(component_id='plot', component_property='figure'),
	[Input(component_id='choosex', component_property='value'),
	Input(component_id='choosey', component_property='value'),
	Input(component_id='fromyear', component_property='value'),
	Input(component_id='toyear', component_property='value')]
)
def update_plot(plotx, ploty, fromyear, toyear):
	# print(plotx + " x " + ploty + " de " + fromyear + " até " + toyear)
	fig = px.bar(extractPlotData(plotx, ploty, fromyear, toyear), title="{0} x {1} de {2} até {3}".format(str(plotx), str(ploty), str(fromyear), str(toyear)),)
	fig.update_xaxes(title=plotx)
	fig.update_yaxes(title=ploty) 

app.run_server(debug=True)