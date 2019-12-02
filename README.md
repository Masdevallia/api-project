# <p align="center">Chat sentiment analysis service</p>

## <p align="center">Ironhack's Data Analytics Bootcamp Project IV: APIs and Cloud Databases</p>

The main goal of this project was to create an API to store and analyze chat messages and create sentiment metrics.

### Sub-objectives:

* Write an API in **bottle** to store chat messages in a database: **Mongodb**.
* Extract sentiment from chat messages and perform a report over a whole conversation: **NLTK sentiment analysis**.
* Deploy the service with **Docker** to **Heroku** and store messages in a cloud database: **MongoDB Atlas**.
* Recommend friends to a user based on the contents from chat 'documents' using a **recommender system with NLP analysis**.

### Results:

The chat sentiment analysis API I developed can be found at: http://chatsentimentapi.herokuapp.com/. It offers real-time access to the chats database, stored in MongoDB Atlas.

### Endpoints Overview:

The examples below show you how to make API calls.

The API has two different types of endpoints:
* Method **Get**: To get information from the API.
* Method **Post**: To add new information to the database.

Description | Method | Request | Parameters | Example
----------- | ------ | ------- | ---------- | ------------
Get chat messages | GET | [/chat/<chat_id>/list](http://chatsentimentapi.herokuapp.com/chat/0/list) | chat_id | 0
Get sentiment from messages | GET | [/chat/<chat_id>/sentiment](http://chatsentimentapi.herokuapp.com/chat/0/sentiment) | chat_id | 0
Get user recommendations | GET | [/user/<user_id>/recommend](http://chatsentimentapi.herokuapp.com/user/0/recommend) | user_id | 1
Create a new user | POST | [/user/create](http://chatsentimentapi.herokuapp.com/user/create) | username | {'username': 'Edward Bloom'}
Create a new chat | POST | [/chat/create](http://chatsentimentapi.herokuapp.com/chat/create) | users array | {'users': '[8, 9, 10]'}
Add a user to an existing chat | POST | [/chat/<chat_id>/adduser](http://chatsentimentapi.herokuapp.com/chat/0/adduser) | chat_id, user_id | 0, {'userId': 1}
Add a message to an existing chat | POST | [/chat/<chat_id>/addmessage](http://chatsentimentapi.herokuapp.com/chat/0/addmessage) | chat_id, message | 0, {'user':0, 'message':'Hi!'}



Example requests from python using the requests package:

```
import requests
# Get chat messages:
chat_id = 0
messages = requests.get(f'http://chatsentimentapi.herokuapp.com/chat/{chat_id}/list').json()

# Get sentiments from messages:
chat_id = 0
sentiments = requests.get(f'http://chatsentimentapi.herokuapp.com/chat/{chat_id}/sentiment').json()

# Get user recommendations:
user_id = 1
recommendations = requests.get(f'http://chatsentimentapi.herokuapp.com/user/{user_id}/recommend').json()

# Add a new user:
newuser = {'username': 'Edward Bloom'}
users = requests.post('http://chatsentimentapi.herokuapp.com/user/create', data=newuser).json()

# Add a new chat:
newchat = {'users': '[8, 9, 10]'}
chats = requests.post('http://chatsentimentapi.herokuapp.com/chat/create', data=newchat).json()

# Add a user to an existing chat:
chat_id = 1
user = {'userId': 1}
usertochat = requests.post(f'http://chatsentimentapi.herokuapp.com/chat/{chat_id}/adduser', data=user).json()

# Add a message to an existing chat:
chat_id = 0
message = {'user':0, 'message':'Hi!'}
newMessage = requests.post(f'http://chatsentimentapi.herokuapp.com/chat/{chat_id}/addmessage', data=message).json()

```