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
						if index>=len(df): print(index) 
						for j in range(0, len(lines[i])):
							df[index].append(lines[i][j])
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
	return
main() 