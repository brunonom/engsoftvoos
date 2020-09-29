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
	last_row = int(0)

	# ['Sigla  da Empresa', 'Número do Voo', 'D I', 'Tipo de Linha',
  #  'Aeroporto Origem', 'Aeroporto Destino', 'Partida Prevista',
  #  'Partida Real', 'Chegada Prevista', 'Chegada Real', 'Situação',
  #  'Justificativa'],
	for a in anos:
		for m in meses:
			path = 'voos/' + a + '/' + m + '.csv'
			data = pandas.read_csv(path, encoding="latin-1", delimiter=";", low_memory = False)
			if a == '2015' and m == '01': # inicializa o csv completo
				data = data.rename(
					columns = {
					data.columns[0] : 'Empresa', 
					data.columns[1] : 'Numero do Voo',
					data.columns[10]: 'Situacao'
					})
				data.to_csv(final_path)
				last_row = int(data.index[-1])
			else: # adiciona no final das colunas
				data = data.rename(lambda i : last_row + i + 1)
				data.to_csv(final_path, mode = 'a', header = False)
				last_row = int(data.index[-1])
			#print(data.iloc[0:, 0])

main()