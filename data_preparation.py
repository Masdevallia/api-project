
# Importing packages:
from pymongo import MongoClient
import json
import os
import pandas as pd
from src.mongo import connectCollection
from dotenv import load_dotenv
load_dotenv()
from bson import json_util

def main():

    # Importing original messages data to MongoDB:
    db, coll = connectCollection('chats','messages')
    with open('./input/original.json', encoding="utf8") as f:
        chats_json = json.load(f)
    coll.insert_many(chats_json)

    # Users collection:
    df = pd.read_json('./input/original.json')
    userDF = df[['idUser','userName']]
    userDF.drop_duplicates(inplace=True)
    coll2 = db['users']
    coll2.insert_many(userDF.to_dict('records'))
    # userDF.to_json('./input/users.json', orient="records")

    # Adding users_id to messages collection:
    db, coll = connectCollection('chats','users')
    data = list(coll.find({}))
    user_id_list = []
    for i in range(len(df)):
        for e in data:
            if df.at[i,'idUser'] == e['idUser']:
                user_id_list.append(e['_id'])
    df['user_id'] = user_id_list
    coll3 = db['messages_linked']
    coll3.insert_many(df.to_dict('records'))

    # Chats collection:
    chatsDF = df[['idChat', 'idUser']]
    chatsDF.drop_duplicates(inplace=True)
    chatsDF.reset_index(drop=True, inplace=True)
    uniqueChats = list(set(chatsDF['idChat']))
    users_total = []
    for e in uniqueChats:
        users = []
        for i in range(len(chatsDF)):
            if chatsDF.at[i,'idChat'] == e:
                users.append(chatsDF.at[i,'idUser'])
        users_total.append(str(users))
    chatsDF = pd.DataFrame(uniqueChats, columns=['idChat'])
    chatsDF['users'] = users_total
    coll4 = db['chats']
    coll4.insert_many(chatsDF.to_dict('records'))
    # chatsDF.to_json('./input/chatsID.json', orient="records")

    # Backup of collections:
    db, coll = connectCollection('chats','messages_linked')
    data = list(coll.find({}))
    with open('./input/messages.json', 'w') as file:
        json.dump(data, file, default=json_util.default)

    db, coll = connectCollection('chats','users')
    data = list(coll.find({}))
    with open('./input/users.json', 'w') as file:
        json.dump(data, file, default=json_util.default)

    db, coll = connectCollection('chats','chats')
    data = list(coll.find({}))
    with open('./input/chats.json', 'w') as file:
        json.dump(data, file, default=json_util.default)


if __name__=="__main__":
    main()