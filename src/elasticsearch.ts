import * as elasticsearch from "elasticsearch";

export const elastic = new elasticsearch.Client({
	host: "https://elasticsearch.tironi.co",
});

export enum Index {
	flights = "flights",
}

export async function createIndex(index: Index): Promise<void> {
	await elastic.indices.create({
		index,
		body: {
			settings: {
				index : {
					number_of_replicas: 0,
					number_of_shards: 1,
				},
			},
		},
	});
}

export async function insert(index: Index, items: any[]): Promise<void> {
	const bulk = [];

	for (const item of items) {
		bulk.push({
			index:  {
				_index: index,
				_type: "_doc",
				_id: item.id,
			},
		});

		bulk.push(item);
	}

	if (bulk.length === 0) {
		return;
	}

	await elastic.bulk({
		body: bulk,
	});
}

export async function deleteIndex(index: Index): Promise<void> {
	await elastic.indices.delete({
		index,
	});
}

export async function ping(): Promise<any> {
	return await elastic.ping({});
}
