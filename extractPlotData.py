import pandas

def extractPlotData(xaxis, yaxis, fromyear, toyear):
	anos = []
	for i in range(fromyear, toyear+1):
		anos.append(str(i))
	
	meses = []
	for i in range(1, 13):
		if i >= 10:
			meses.append(str(i))
		else:
			meses.append('0' + str(i))

	columns = ["Indice",
			"Empresa",
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

	xcolnum = 0
	ycolnum = 0
	for i in range(0, len(columns)):
		if columns[i] == xaxis:
			xcolnum = i
		if columns[i] == yaxis:
			ycolnum = i

	df = [[xaxis, yaxis]]

	for a in anos:
		for m in ["01"]:
			path = 'voos/' + a + '/' + m + '.csv'
			file = open(path, "r", encoding="latin-1")
			# print(path)

			sep = ""
			for line in file:
				for char in line:
					if char == '\t':
						sep = '\t'
					if char == ',':
						sep = ','
					if char == ';':
						sep = ';'
				break

			# if sep == "":
			# 	print("\tfailed to recognize separator.")
			# 	return
			# else:
			# 	print("\tseparator is {0}.".format(sep))

			file.seek(0)
			lines = file.readlines()
			pastHeader = False
			for i in range(0, len(lines)):
				lines[i] = lines[i].replace('"', '').replace('\n', '').split(sep)

				if not pastHeader:
					if ((lines[i][6] == "Partida Prevista") or 
						(lines[i][6] == "dt_partida_prevista") or 
						(lines[i][6] == "Data Partida Prevista")):
						pastHeader = True
						# print("\tpassed header on line {0}.".format(i+1))
				else:
					df.append([lines[i][xcolnum], lines[i][ycolnum]])

			file.close()

	temp = open("temp.csv", "w")
	for i in df:
		for j in i:
			temp.write(str(j) + ';')
		temp.write("\n")
	temp.close()

	dataframe = pandas.read_csv("temp.csv", delimiter=";")
	print("aaa")
	return dataframe
