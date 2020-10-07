import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from getDataframe import getDataframe
from dash.dependencies import Input, Output
from extractPlotData import extractPlotData

# print("hello")
# df = getDataframe()
# print("dun")
# empresaSum = df.groupby(["Empresa"]).sum().reset_index()
# print(df[2])
# exit()

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

dates = []
for i in range(2015, 2020):
	for j in range(1, 13):
		dates.append([j,i])

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
		], style={'width': '40%', 'display': 'inline-block'}
	),

	html.Div([
		# html.Label("De", htmlFor="from"),
		dcc.Dropdown(
			id="from",
			options=[{"label": str(i), "value": str(i)} for i in dates],
			value=str(dates[0])
			),
		# html.Label("Até", htmlFor="to"),
		dcc.Dropdown(
			id="to",
			options=[{"label": str(i), "value": str(i)} for i in dates],
			value=str(dates[0])
			),
		], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}
	),

	dcc.Graph(
		id="plot",
		figure=px.scatter(
			extractPlotData("Empresa", "Empresa", 1, 2015, 1, 2015),
			title="Empresa x Empresa de 1/2015 até 1/2015",
			x="Empresa",
			y="Empresa",
		)
	),
])

@app.callback(
	Output('plot', 'figure'),
	[
	Input('choosex', 'value'),
	Input('choosey', 'value'),
	Input('from', 'value'),
	Input('to', 'value')
	]
)
def update_plot(plotx, ploty, fromdate, todate):
	# print(plotx + " x " + ploty + " de " + fromyear + " até " + toyear)
	fromsplit = fromdate.replace('[', '').replace(']', '').replace(' ', '').split(",")
	tosplit = todate.replace('[', '').replace(']', '').replace(' ', '').split(",")
	df = extractPlotData(plotx, ploty, int(fromsplit[0]), int(fromsplit[1]), int(tosplit[0]), int(tosplit[1]))
	fig = px.scatter(df, x=plotx, y=ploty,
		title="{} x {} de {}/{} até {}/{}".format(str(plotx), str(ploty), fromsplit[0], fromsplit[1], tosplit[0], tosplit[1]),)
	fig.update_xaxes(title=plotx)
	fig.update_yaxes(title=ploty) 
	return fig

@app.callback(
	[
	Output('to', 'value'),
	Output('to', 'options'),
	],
	[
	Input('from', 'value')
	]
)
def update_possible_dates(fromvalue):
	tovalue = fromvalue
	for i in range(len(dates)):
		if str(dates[i])==fromvalue:
			tooptions = [{'label': str(j), 'value': str(j)} for j in dates[i::]]
			break
	return tovalue, tooptions



app.run_server(debug=True)