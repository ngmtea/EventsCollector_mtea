import sys
from pymongo import MongoClient
from pymongo import UpdateOne
from blockchainetl.bricher.configs.config import MongoDBConfig


class CreamVenusMongodbStreamingExporter(object):
    def __init__(
        self,
        collection_url: str = MongoDBConfig.LOCAL_CONNECTION_URL,
        db_name: str = MongoDBConfig.LOCAL_BRICHER_DAPPS_DATABASE,
        # collection_name: str = MongoDBConfig.LOCAL_CREAM_VENUS_EVENTS_COLLECTION,
        # collection_name: str = MongoDBConfig.LOCAL_CREAM_EVENTS_COLLECTION,
        collection_name: str = MongoDBConfig.LOCAL_VENUS_EVENTS_COLLECTION,
    ) -> None:
        try:
            # FIXME Unable to read from .env file
            self.client: MongoClient = MongoClient(collection_url)
        except:
            sys.exit(1)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def export_items(self, items: list) -> None:
        self.export_events(items)

    def export_events(self, operations_data: list) -> None:
        if not operations_data:
            return

        bulk_operation = [
            UpdateOne({"_id": data["_id"]}, {"$set": data}, upsert=True)
            for data in operations_data
        ]

        try:
            self.collection.bulk_write(bulk_operation)
        except Exception as bwe:
            print(bwe)

    def delete_events_for_testing(self):
        filter: dict = {"block_number": {"$lte": 21175364}}
        self.collection.delete_many(filter=filter)
