
from bottle import route, run, get, post, request
import bson
import os
import json
from dotenv import load_dotenv
load_dotenv()
from src.mongo import connectCollection
from src.sentiment import sentimentAnalyzer


def main():


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


    @post('/chat/create')
    def createChat(user_id):
        '''
        Creates a conversation to load messages
        input: An array of user ids
        output: chat_id
        '''
        return None


    @post('/chat/<chat_id>/adduser')
    def addUserToChat(chat_id, user_id):
        '''
        Adds a user to a chat (just in case you want to add more users to a chat after it's creation)
        input: user_id
        output: user_id, chat_id
        '''
        return None


    @post('/chat/<chat_id>/addmessage')
    def addMessageToChat(chat_id, user_id, message):
        '''
        Adds a message to an existing chat
        input: chat_id, user_id, message
        output: message_id
        '''
        # Help: Before adding the chat message to the database, check that the incoming user is part of 
        # this chat id. If not, raise an exception.
        return None


    @get("/")
    def index():
        return 'Welcome to the chat sentiment analysis API'


    @get('/chat/<chat_id>/list')
    def getMessages(chat_id):
        '''
        Get all messages from 'chat_id'
        input: chat_id
        output: json array with all messages from this chat_id
        '''
        db, coll = connectCollection('chats','messages_linked')
        query = {'idChat': int(chat_id)}
        test_query = coll.find(query)
        messages = {}
        for index,dictionary in enumerate(test_query):
            index += 1
            messages[f'message_{index}'] = dictionary['text']
        return messages


    @get('/chat/<chat_id>/sentiment')
    def getSentiment(chat_id):
        '''
        Analyzes messages from chat_id. Uses 'NLTK' sentiment analysis package for this task.
        input: chat_id
        output: json with all sentiments from messages in the chat
        '''
        messages = getMessages(chat_id)
        messagesSentiment = sentimentAnalyzer(messages)
        return messagesSentiment


    @get('/user/<user_id>/recommend')
    def recommendUsers(user_id):
        '''
        Recommends a friend to a user based on chat contents
        input: user_id
        output: json array with top 3 similar users
        '''

        return None


    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP','0.0.0.0')
    run(host=host, port=port, debug=True)
    # run(host='0.0.0.0', port=8080, debug=True)
    # run(host='localhost', port=8080)


if __name__=="__main__":
    main()