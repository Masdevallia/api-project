
# Importing packages:
from pymongo import MongoClient
import json
import os
import pandas as pd
from src.mongo import connectCollection
from dotenv import load_dotenv
load_dotenv()

# Connecting to MongoDB Atlas:
password = os.getenv("ATLAS_MONGO_PASS")
connection = "mongodb+srv://masdevallia:{}@clusterdataanalysis-9nklb.mongodb.net/test?retryWrites=true&w=majority".format(password)

# Importing original messages data to MongoDB:
client = MongoClient(connection)
db, coll = connectCollection('chats','messages')
with open('./input/chats.json', encoding="utf8") as f:
    chats_json = json.load(f)
coll.insert_many(chats_json)

# Dataframe:
df = pd.read_json('./input/chats.json')

# Users collection: 
userDF = df[['idUser','userName']]
userDF.drop_duplicates(inplace=True)

# Importing users data to MongoDB:
coll2 = db['users']
coll2.insert_many(userDF.to_dict('records'))

userDF.to_json('./input/users.json', orient="records")

# Adding users_id to messages collection:
db, coll = connectCollection('chats','users')

data = list(coll.find({}))

user_id_list = []
for i in range(len(df)):
    for e in data:
        if df.at[i,'idUser'] == e['idUser']:
            user_id_list.append(e['_id'])

df['user_id'] = user_id_list

# Importing new messages data to MongoDB:
coll3 = db['messages_linked']
coll3.insert_many(df.to_dict('records'))