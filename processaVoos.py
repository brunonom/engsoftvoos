import pandas
import numpy as np
from helpers import minutesDiff

delay_final = pandas.DataFrame(
	columns = [
	"Empresa",
	"Partida Delay Total", # pra empresa e tvz aeroporto
	"Chegada Delay Total", # pra empresa e tvz aeroporto
	"Quantidade de voos"
	])
visto = {}
idx = 0
updates = {}
def processa_delay(mat):
	global delay_final
	global visto
	global idx
	global updates
	row = 0
	for x in mat:
		row+=1
		name = x[0]
		if not name in visto:
			nv = pandas.DataFrame([[name, 0.0, 0.0, 0]],
					columns = [
					"Empresa",
					"Partida Delay Total", 
					"Chegada Delay Total",
					"Quantidade de voos"
					]
				)
			delay_final = delay_final.append(nv, ignore_index = True)
			visto[name] = idx
			updates[name] = [0, 0, 0]
			idx += 1
		updates[name] = np.add(updates[name], [minutesDiff(x[6], x[7]), minutesDiff(x[8], x[9]), 1])

		#updates[name] += 
		

anos = []
for i in range(2015, 2020):
	anos.append(str(i))
meses = []
for i in range(1, 13):
	if i >= 10:
		meses.append(str(i))
	else:
		meses.append('0' + str(i))
cols = ["Partida Delay Total", "Chegada Delay Total", "Quantidade de voos"]
for a in anos:
	for m in meses:
		read_path = "voos/" + a + '/' + m + '.csv'
		df = pandas.read_csv(
			read_path,
			low_memory = False,
			delimiter=";",
			encoding = "latin-1",
			skipinitialspace = True,
		)
		df = df.rename(columns={
		  df.columns[0] : "Empresa",
		  df.columns[1] : "Numero Voo",
		  df.columns[2] : "Codigo DI",
		  df.columns[3] : "Codigo Tipo Linha",
		  df.columns[4] : "Origem",
		  df.columns[5] : "Destino",
		  df.columns[6] : "Partida Prevista",
		  df.columns[7] : "Partida Real",
		  df.columns[8] : "Chegada Prevista",
		  df.columns[9] : "Chegada Real",
		  df.columns[10] : "Situacao",
		  df.columns[11] : "Justificativa"
		})
		#processa o csv e altera o dataframe final
		processa_delay(df.to_numpy())
		for x in updates:
			for j in range(3):
				delay_final.loc[visto[x], cols[j]] = updates[x][j]
		delay_final.to_csv("lol.csv")
		exit()
