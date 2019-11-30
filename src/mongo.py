
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

password = os.getenv("ATLAS_MONGO_PASS")
connection = "mongodb+srv://masdevallia:{}@clusterdataanalysis-9nklb.mongodb.net/test?retryWrites=true&w=majority".format(password)
client = MongoClient(connection)

def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll

