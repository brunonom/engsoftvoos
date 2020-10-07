import pandas
def main():
	anos = []
	for i in range(2015, 2020):
		anos.append(str(i))
	meses = []
	for i in range(1, 13):
		if i >= 10:
			meses.append(str(i))
		else:
			meses.append('0' + str(i))
	final_path = 'voos/complete.csv'
	# last_row = int(0)

	# ['Sigla  da Empresa', 'Número do Voo', 'D I', 'Tipo de Linha',
  #  'Aeroporto Origem', 'Aeroporto Destino', 'Partida Prevista',
  #  'Partida Real', 'Chegada Prevista', 'Chegada Real', 'Situação',
  #  'Justificativa'],
	# for a in anos:
	# 	for m in meses:
	# 		path = 'voos/' + a + '/' + m + '.csv'
	# 		data = pandas.read_csv(path, encoding="latin-1", delimiter=";", low_memory = False)
	# 		if a == '2015' and m == '01': # inicializa o csv completo
	# 			data = data.rename(
	# 				columns = {
	# 				data.columns[0] : 'Empresa', 
	# 				data.columns[1] : 'Numero do Voo',
	# 				data.columns[10]: 'Situacao'
	# 				})
	# 			data.to_csv(final_path)
	# 			last_row = int(data.index[-1])
	# 		else: # adiciona no final das colunas
	# 			#if(len(data.columns) != 12):
	# 			#	print(a, m)
	# 			data = data.rename(lambda i : last_row + i + 1)
	# 			data.to_csv(final_path, mode = 'a', header = False)
	# 			last_row = int(data.index[-1])
	# 		#print(data.iloc[0:, 0])

	df = [[	"Indice",
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
			"Justificativa"]]

	# print([df[0]])

	# final = open(final_path, "w")
	# for i in df[0]:
	# 	final.write(str(i) + ';')
	# final.write("\n")

	for a in anos:
		for m in meses:
			path = 'voos/' + a + '/' + m + '.csv'
			print(path)
			
			file = open(path, "r", encoding="latin-1")

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

			index = 1
			indexed = False
			file.seek(0)
			lines = file.readlines()
			pastHeader = False
			for i in range(0, len(lines)):
				lines[i] = lines[i].replace('"', '').replace('\n', '').split(sep)

				if not pastHeader:
					for j in lines[i]:
						if j=="Indice":
							pastHeader = True
							indexed = True
							# print("\tpassed header on line {0}.".format(i+1))
							# print("\tindexed")
						elif ((j == "Partida Prevista") or 
							(j == "dt_partida_prevista") or 
							(j == "Data Partida Prevista")):
							pastHeader = True
							# print("\tpassed header on line {0}.".format(i+1))
							# print("\tnot indexed")
							break
				else:
					# valid_row = True
					# for j in lines[i]:
					# 	if not j or j.isspace():
					# 		valid_row = False
					# 		break
							
					# if valid_row:		
						df.append([index])
						# final.write(str(index) + ';')
						if index>=len(df): print(index) 
						for j in range(0, len(lines[i])):
							# final.write(str(lines[i][j]) + ';')
							df[index].append(lines[i][j])
						# final.write("\n")
						index += 1

			if not indexed:
				file = open(path, "w")
				for i in range(0, len(df)):
					for j in range(0, len(df[i])):
						if j==len(df[i])-1:
							file.write(str(df[i][j]))
						else:
							file.write(str(df[i][j]) + ';')
					file.write("\n")

				file.close()

			df = [df[0]]

	# for i in range(0, len(df)):
	# 	for j in range(0, len(df[i])):
	# 		final.write(str(df[i][j]) + ';')
	# 	final.write("\n")
	# final.close()

	return

main() 