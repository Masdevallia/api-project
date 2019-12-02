
from bottle import route, run, get, post, request
import bson
import json
import re
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
# nltk.download('punkt')
# nltk.download('stopwords')
from src.mongo import connectCollection
from src.sentiment import *
from src.recommender import similarityDF

import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')


def main():


    # Create a new user:
    @get('/user/create')
    def userForm():
        return '''<form method="post" action="/user/create">
                    Insert the new user's name: <input name="username" type="text" />
                    <input type="submit" />
                </form>'''

    @post('/user/create')
    def createUser():
        '''
        Creates a user and saves it into the database
        input: the user's name (dic): e.g. {'username': 'Cristina Rota'}
        output: user_id
        '''
        username = str(request.forms.get('username'))
        db, coll = connectCollection('chats','users')
        data = list(coll.aggregate([{'$project':{'idUser':1}}]))
        newUser = {'idUser':max([e['idUser'] for e in data])+1, 'userName': username}
        # Checking that the given username does not already exist in the database:
        takenNames = list(coll.aggregate([{'$project':{'userName':1}}]))
        if newUser['userName'] in [e['userName'] for e in takenNames]:
            error = 'Sorry, there is already a user with that exact name in the database'
            return {'Exception':error}
        else:
            # Inserting new user to the database:
            user_id = coll.insert_one(newUser).inserted_id
            return {'ObjectId': str(user_id), 'UserId': newUser['idUser']}


    # Create a new chat:
    @get('/chat/create')
    def chatForm():
        return '''<form method="post" action="/chat/create">
                    Insert an array of user ids (e.g. [8, 10]): <input name="users" type="text" />
                    <input type="submit" />
                </form>'''

    @post('/chat/create')
    def createChat():
        '''
        Creates a conversation to load messages
        input: A dictionary containing an array of user ids: e.g. {'users': '[8, 9, 10]'}
        output: chat_id
        '''
        users = str(request.forms.get('users'))
        print(users)
        db, coll = connectCollection('chats','chats')
        data = list(coll.aggregate([{'$project':{'idChat':1}}]))
        newChat = {'idChat':max([e['idChat'] for e in data])+1, 'users': users}
        print(newChat)
         # Checking if users exist in the database
        db2, coll2 = connectCollection('chats','users')
        usersData = list(coll2.aggregate([{'$project':{'idUser':1}}]))
        chatUsers = [int(e) for e in re.sub('\[|\]','',newChat['users']).split(', ')]
        for e in chatUsers:
            if e not in [f['idUser'] for f in usersData]:
                error = 'Sorry, one or more of the users you are trying to include do not exist in the database. You must create them first.'
                return {'Exception':error}
        # Inserting new chat to the database:
        chat_id = coll.insert_one(newChat).inserted_id
        return {'ObjectId': str(chat_id), 'ChatId': newChat['idChat']}


    # Add a user to an existing chat:
    @post('/chat/<chat_id>/adduser')
    def addUserToChat(chat_id):
        '''
        Adds a user to a chat (just in case you want to add more users to a chat after it's creation)
        input: the user's id (dic): e.g. {'userId': 0}
        output: user_id, chat_id
        '''
        db, coll = connectCollection('chats','chats')
        data = list(coll.find({'idChat': int(chat_id)}))
        # Checking if chat exists:
        if len(data) == 0:
            error = "Sorry, this chat doesn't exist. You must create it first."
            return {'Exception':error}
        user = int(request.forms.get('userId'))
        db2, coll2 = connectCollection('chats','users')
        usersData = list(coll2.aggregate([{'$project':{'idUser':1}}]))
        # Checking if user exists:
        if user not in [e['idUser'] for e in usersData]:
            error = 'Sorry, the user you are trying to include does not exist in the database. You must create it first.'
            return {'Exception':error}
        users = [int(e) for e in re.sub('\[|\]','',data[0]['users']).split(', ')]        
        # Checking if user is already part of the chat:
        if user in users:
            error = 'Sorry, this user is already part of the chat'
            return {'Exception':error}
        users.append(user)
        # Adding the new user to the chat:
        coll.update_one({'idChat': int(chat_id)}, {'$set':{'users':str(users)}})
        return {'UserId': user, 'ChatId': int(chat_id)}


    # Add a message to an existing chat:
    @post('/chat/<chat_id>/addmessage')
    def addMessageToChat(chat_id):
        '''
        Adds a message to an existing chat
        input: chat_id / user_id and message as dict: e.g. {'user':0, 'message':'Hi!'}
        output: message_id
        '''
        db, coll = connectCollection('chats','messages_linked')
        data = list(coll.find({'idChat': int(chat_id)}))
        user = int(request.forms.get('user'))
        message = str(request.forms.get('message'))
        # Checking if the chat exists
        db2, coll2 = connectCollection('chats','chats')
        chat = list(coll2.find({'idChat': int(chat_id)}))
        if len(chat) == 0:
            error = "Sorry, this chat doesn't exist. You must create it first."
            return {'Exception':error}
        # Checking that the incoming user is part of this chat before adding the chat message to the database.
        chatUsers = [int(e) for e in re.sub('\[|\]','',chat[0]['users']).split(', ')]
        if user not in chatUsers:
            error = 'Sorry, this user is not part of the chat. You must add him/her first.'
            return {'Exception':error}
        # Adding the new message:
        db3, coll3 = connectCollection('chats','users')
        selectedUser = list(coll3.find({'idUser': user}))
        if len(data) == 0:
            newMessageId = 0
        else:
            newMessageId = max([e['idMessage'] for e in data])+1
        newMessage = {'datetime': datetime.datetime.utcnow(),
                        'idChat': int(chat_id),
                        'idMessage': newMessageId,
                        'idUser': user,
                        'text': message,
                        'userName': selectedUser[0]['userName'],
                        'user_id': selectedUser[0]['_id']}
        message_id = coll.insert_one(newMessage).inserted_id
        return {'ObjectId': str(message_id), 'MessageId': newMessage['idMessage']}
        

    # Index:
    @get("/")
    def index():
        return 'Welcome to the chat sentiment analysis API'


    # Get all messages from a chat:
    @get('/chat/<chat_id>/list')
    def getMessages(chat_id):
        '''
        Get all messages from 'chat_id'
        input: chat_id
        output: json array with all messages from this chat_id
        '''
        db, coll = connectCollection('chats','messages_linked')
        data = list(coll.find({'idChat': int(chat_id)}))
        messages = {}

        for index,dictionary in enumerate(data):
            index += 1
            messages[f'message_{index}'] = {'user': dictionary['userName'],
                                            'date': str(dictionary['datetime'])[0:10],
                                            'time': str(dictionary['datetime'])[11:19],
                                            'text': dictionary['text']}
        if len(messages) == 0:
            error = 'Sorry, this chat does not exist in the database'
            return {'Exception':error}
        else:
            return messages


    # Sentiment analyzer:
    @get('/chat/<chat_id>/sentiment')
    def getSentiment(chat_id):
        '''
        Analyzes messages from chat_id. Uses 'NLTK' sentiment analysis package for this task.
        input: chat_id
        output: json with all sentiments from messages in the chat
        '''
        messages = getMessages(chat_id)
        if 'Exception' in messages:
            return messages
        else:
            messagesSentiment = sentimentAnalyzer(messages)
            plotSentiments(messagesSentiment)
            return messagesSentiment


    # User recommender:
    @get('/user/<user_id>/recommend')
    def recommendUsers(user_id):
        '''
        Recommends a friend to a user based on chat contents
        input: user_id
        output: json array with top 3 similar users
        '''
        db, coll = connectCollection('chats','messages_linked')
        data = list(coll.find({}))
        # Checking if the user exists in the database:
        if int(user_id) not in list(set([e['idUser'] for e in data])):
            error = 'Sorry, this user does not exist in the database'
            return {'Exception':error}
        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = set(stopwords.words('english'))       
        TokensDict = {}
        for userId in list(set([e['idUser'] for e in data])):
            usersData = list(coll.find({'idUser': userId}))
            usersTokens = [tokenizer.tokenize(e['text']) for e in usersData]
            usersTokens_clean = [word for message in usersTokens for word in message if word not in stop_words]
            TokensDict[f'{userId}'] = ' '.join(usersTokens_clean)
        sim_df = similarityDF(TokensDict)
        recommendedIds = [int(e) for e in list(sim_df[str(user_id)].sort_values(ascending=False)[0:3].index)]
        db2, coll2 = connectCollection('chats','users')
        recommendedNames = []
        for e in recommendedIds:
            userInfo = list(coll2.find({'idUser': e}))
            recommendedNames.append(userInfo[0]['userName'])
        return {'recommended_users_ids': recommendedIds,
                'recommended_users_names': recommendedNames}
        

    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP','0.0.0.0')
    run(host=host, port=port, debug=True)
    # run(host='0.0.0.0', port=8080, debug=True)
    # run(host='localhost', port=8080)


if __name__=="__main__":
    main()