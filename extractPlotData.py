import pandas

def extractPlotData(xaxis, yaxis, frommonth, fromyear, tomonth, toyear):
	print(xaxis, yaxis, frommonth, fromyear, tomonth, toyear)
	dates = []
	for i in range(2015, 2020):
		if i==fromyear:
			if i==toyear:
				for j in range(frommonth, tomonth+1):
					dates.append([str(j),str(i)])
				break	
			for j in range(frommonth, 13):
				dates.append([str(j),str(i)])
		elif i>fromyear and i<toyear:
			for j in range(1, 13):
				dates.append([str(j),str(i)])
		elif i==toyear:
			for j in range(1, tomonth+1):
					dates.append([str(j),str(i)])

	for d in dates:
		if int(d[0])<10:
			d[0] = '0' + d[0]

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

	if xaxis == yaxis:
		df = [[str(xaxis)]]
	else:
		df = [[str(xaxis), str(yaxis)]]
	
	# print("fetching data...")
	for d in dates:
		path = 'voos/' + d[1] + '/' + d[0] + '.csv'
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
		for i in range(1, len(lines)):
			lines[i] = lines[i].split(sep)
			df.append([lines[i][xcolnum], lines[i][ycolnum]])
		file.close()
	# print("complete")

	# print("to pandas...")
	temp = open("temp.csv", "w")
	for i in df:
		for j in range(0, len(i)):
			if j==len(i)-1:
				temp.write(str(i[j]))
			else:
				temp.write(str(i[j]) + ';')
		temp.write("\n")
	temp.close()

	dataframe = pandas.read_csv("temp.csv", delimiter=";", low_memory=False)
	# print("complete")

	# print(dataframe)

	return dataframe
