# This will be used to import tokens hash from MongoDB database.
import sys
from pymongo.cursor import Cursor
from pymongo import MongoClient
from typing import List

from configs.config import MongoDBConfig


class MongoStreamingImporter(object):
    def __init__(
            self,
            collection_url_importer: str = MongoDBConfig.CONNECTION_URL,
            db_name: str = MongoDBConfig.BRICHER_DATABASE,
            collection_name: str = MongoDBConfig.DAPPS_COLLECTION,
    ):
        try:
            # FIXME Unable to read from .env file
            self.client: MongoClient = MongoClient(collection_url_importer)
        except:
            sys.exit(1)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_cream_venus_token_address(self, project_name):
        result: list = []

        # NOTE: For now, due to problems with DUNE, only Venus events are crawled.
        # cream_collection: Cursor = self.collection.find({"projectName": "Cream"})
        # for c in cream_collection:
        #     for reserve in c["reservesList"]:
        #         result.append(c["reservesList"][reserve]["cToken"])

        cream_collection: Cursor = self.collection.find({"projectName": project_name})
        for v in cream_collection:
            for reserve in v["reservesList"]:
                result.append(v["reservesList"][reserve]["cToken"])

        return result
