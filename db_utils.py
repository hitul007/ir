import time
import datetime

import motor.motor_asyncio

MONGO_DB_NAME = 'irage'
MONGO_DB_CONN_STRING = "mongodb://localhost:27017"


class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class MongoDB(Singleton):
    def __init__(self):
        self.db = None
        self.create_connection()

    def create_connection(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_CONN_STRING)
        db = client[MONGO_DB_NAME] 
        self.db = db
 
    def get_instance(self):
        return self.db


def get_price_collection_name():
    # TODO: datetime.datetime.now() can take longer time and can affect response time. 
    # TODO: We can cache it with timer.

    # TODO: Create index on uuid field
    return '_'.join(['price_data', datetime.datetime.now().strftime('%d_%m_%Y')])


async def insert_uuid(db, uuid):
    collection_name = get_price_collection_name()
    await db[collection_name].insert_one({
        'uuid': uuid,
        'timestamp': time.time()
    })
  
