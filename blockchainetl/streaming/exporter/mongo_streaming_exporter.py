import logging
from pymongo import UpdateOne
import time
from pymongo import MongoClient
from configs.config import MongoDBConfig

logger = logging.getLogger("MongodbStreamingExporter")


class MongodbStreamingExporter(object):
    """Manages connection to  database and makes async queries
    """

    def __init__(self, connection_url, collector_id=MongoDBConfig.LENDING_EVENTS, db_prefix="", database=MongoDBConfig.DATABASE):
        self._conn = None
        # url = f"mongodb://{MongoDBConfig.NAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}"
        url = connection_url
        self.mongo = MongoClient(url)
        if db_prefix:
            mongo_db_str = db_prefix + "_" + database
        else:
            mongo_db_str = database
        self.mongo_db = self.mongo[mongo_db_str]
        self.mongo_collectors = self.mongo_db[MongoDBConfig.COLLECTORS]
        if collector_id in MongoDBConfig.EVENTS:
            self.event = self.mongo_db[collector_id]
        elif collector_id in MongoDBConfig.MULTI_SIG_EVENTS:
            self.event = self.mongo_db[MongoDBConfig.MULTI_SIG_EVENTS[collector_id]]
        else:
            self.event = self.mongo_db[MongoDBConfig.LENDING_EVENTS]

        self.collector_id = collector_id

    def get_collector(self, collector_id):
        key = {"id": collector_id}
        collector = self.mongo_collectors.find_one(key)
        if not collector:
            collector = {
                "_id": collector_id,
                "id": collector_id
            }
            self.update_collector(collector)
        return collector

    def get_event_items(self, filter):
        return list(self.event.find(filter))

    def get_items(self, db, collection, filter):
        return self.mongo[db][collection].find(filter)

    def update_collector(self, collector):
        key = {'id': collector['id']}
        data = {"$set": collector}

        self.mongo_collectors.update_one(key, data, upsert=True)

    def update_latest_updated_at(self, collector_id, latest_updated_at):
        key = {'_id': collector_id}
        update = {"$set": {
            "last_updated_at_block_number": latest_updated_at
        }}
        self.mongo_collectors.update_one(key, update)

    def open(self):
        pass

    def export_items(self, items):
        self.export_events(items)

    def export_events(self, operations_data):
        if not operations_data:
            logger.debug(f"Error: Don't have any data to write")
            return
        start = time.time()
        bulk_operations = [UpdateOne({'_id': data['_id']}, {"$set": data}, upsert=True) for data in operations_data]
        logger.info("Updating into events ........")
        try:
            self.event.bulk_write(bulk_operations)
        except Exception as bwe:
            logger.error(f"Error: {bwe}")
        end = time.time()
        logger.info(f"Success write events to database take {end - start}s")

    def close(self):
        pass

    def export_collection_items(self, db, collection, operations_data):
        if not operations_data:
            logger.debug(f"Error: Don't have any data to write")
            return
        start = time.time()
        bulk_operations = [UpdateOne({'_id': data['_id']}, {"$set": data}, upsert=True) for data in operations_data]
        logger.info(f"Updating into collection {collection} ........")
        try:
            self.mongo[db][collection].bulk_write(bulk_operations)
        except Exception as bwe:
            logger.error(f"Error: {bwe}")
        end = time.time()
        logger.info(f"Success write data to database take {end - start}s")