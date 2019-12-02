
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

connection = os.getenv("ATLAS_MONGO_CONNECTION")
client = MongoClient(connection)

def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll
