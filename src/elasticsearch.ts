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

export async function insert(index: Index, entities: any[]): Promise<void> {
	const body = [];

	for (const entity of entities) {
		body.push({
			index:  {
				_index: index,
				_type: "_doc",
				_id: entity.id,
			},
		});

		body.push(entity);
	}

	if (body.length === 0) {
		return;
	}

	await elastic.bulk({
		body,
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
