import azure.cosmos.cosmos_client as cosmos_client

import utils.config as config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']


class MyCosmosClient:
    def __init__(self):
        client = cosmos_client.CosmosClient(HOST, {"masterKey": MASTER_KEY})
        self._client = client
        self._db = self._client.get_database_client(config.settings['database_id'])
        self._container = self._db.get_container_client(config.settings['container_id'])

    def client(self):
        return self._client

    def get_database(self, database_id):
        return self._db

    def query(self, query_str):
        return self._container.query_items(query_str, enable_cross_partition_query=True)

    def query_all_items(self):
        query_str = 'select * from c'
        return self.query(query_str)

    def insert(self, item):
        return self._container.upsert_item(item)


def main():
    client = MyCosmosClient()
    items = client.query('select * from c where c.id="az test"')
    for item in items:
        print(item)
    test_case = {
        'id': 'az test',
        'command': 'az test',
        'totalCount': 20,
        'nextCommand': [{'command': 'az next text', 'arguments': ['-a'], 'count':10, 'score':30}]
    }
    ret = client.insert(test_case)
    print("Inserted Item:{}".format(ret))


if __name__ == "__main__":
    main()
