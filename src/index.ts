import moment = require("moment");
import csvParser = require("csv-parser");
import { fs } from "mz";

import * as elasticsearch from "./elasticsearch";

interface IFlight {
	Indice: string;
	Empresa: string;
	'Numero Voo': string;
	'Codigo DI': string;
	'Codigo Tipo Linha': string;
	Origem: string;
	Destino: string;
	'Partida Prevista': string;
	'Partida Real': string;
	'Chegada Prevista': string;
	'Chegada Real': string;
	'Situacao Voo': string;
	Justificativa: string;
}

interface IFormattedFlight {
	Indice: string;
	Empresa: string;
	'Numero Voo': number;
	'Codigo DI': string;
	'Codigo Tipo Linha': string;
	Origem: string;
	Destino: string;
	'Partida Prevista': Date | null;
	'Partida Real': Date | null;
	'Partida Atraso': number | null;
	'Chegada Prevista': Date | null;
	'Chegada Real': Date | null;
	'Chegada Atraso': number | null;
	'Situacao Voo': string;
	Justificativa: string;
}



function formatDate(dateString: string): Date | null {
	try {
		const [ date, time ] = dateString.split(" ");
		const [ day, month, year ] = date.split("/");
		const [ hour, minute ] = time.split(":");

		return new Date(
			Number(year),
			Number(month) - 1,
			Number(day),
			Number(hour),
			Number(minute),
		);
	} catch {
		return null;
	}
}

function dateDiffSeconds(dateA: Date | null, dateB: Date | null): number | null {
	if (!dateA || !dateB) {
		return null;
	}

	return moment(dateA).diff(dateB, "seconds");
}

function formatFlight(flight: IFlight): IFormattedFlight {
	const preFormattedFlight: Omit<Omit<IFormattedFlight, "Partida Atraso">, "Chegada Atraso"> = {
		...flight,
		'Numero Voo': Number(flight["Numero Voo"]),
		'Partida Prevista': formatDate(flight["Partida Prevista"]),
		'Partida Real': formatDate(flight["Partida Real"]),
		'Chegada Prevista': formatDate(flight["Chegada Prevista"]),
		'Chegada Real': formatDate(flight["Chegada Real"]),
	};

	return {
		...preFormattedFlight,
		'Partida Atraso': dateDiffSeconds(
			preFormattedFlight["Partida Prevista"],
			preFormattedFlight["Partida Real"],
		),
		'Chegada Atraso': dateDiffSeconds(
			preFormattedFlight["Chegada Prevista"],
			preFormattedFlight["Chegada Real"],
		),
	}
}

async function uploadCsv(inserted: number, path: string): Promise<number> {
	return await new Promise((res) => {
		const flights: IFlight[] = [];

		fs.createReadStream(path)
			.pipe(csvParser({ separator: ";" }))
			.on("data", (data) => flights.push(data))
			.on("end", async () => {
				const formattedFlights = flights.map(formatFlight);

				function chunkArray(myArray: any[], chunkSize: number){
					var index = 0;
					var arrayLength = myArray.length;
					var tempArray: any[][] = [];

					for (index = 0; index < arrayLength; index += chunkSize) {
						tempArray.push(myArray.slice(index, index + chunkSize));
					}

					return tempArray;
				}

				for (const chunk of chunkArray(formattedFlights, 5000)) {
					await elasticsearch.insert(
						elasticsearch.Index.flights,
						chunk,
					);
				}

				res(inserted + formattedFlights.length);
			});
	})
}

async function streamData(reCreate: boolean = false) {
	if (reCreate) {
		try {
			await elasticsearch.deleteIndex(elasticsearch.Index.flights);
		} catch {
			console.log("Index does not exist");
		}

		await elasticsearch.createIndex(elasticsearch.Index.flights);
	}

	let inserted = 0;

	for (let ano = 2015; ano < 2020; ano++) {
		for (let mes = 1; mes < 13; mes++) {
			console.log(`./voos/${ano}/${mes >= 10 ? mes : `0${mes}`}.csv`)
			inserted = await uploadCsv(inserted, `./voos/${ano}/${mes >= 10 ? mes : `0${mes}`}.csv`);
			console.log(`${inserted} inserted`);
		}
	}
}

streamData()
	.then(console.log)
	.catch(console.error);
