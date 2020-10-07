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

	final_path = 'voos/complete.csv'
	final = open(final_path, "w")
	final.write("Indice;Empresa;Numero Voo;Codigo DI;Codigo Tipo Linha;Origem;Destino;Partida Prevista;Partida Real;Chegada Prevista;Chegada Real;Situacao Voo;Justificativa\n")
	index = 1
	sep = ";"
	for a in anos:
		for m in meses:
			path = 'voos/' + a + '/' + m + '.csv'
			print(path)
			
			file = open(path, "r", encoding="latin-1")
			file.seek(0)

			lines = file.readlines()
			for i in range(1, len(lines)):
				final.write(lines[i])
				index += 1
	final.close()
	return

main()