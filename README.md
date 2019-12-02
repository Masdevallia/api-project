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

Description | Method | Request | Parameters
----------- | ------ | ------- | --------------
Get chat messages | GET | [/chat/<chat_id>/list](http://chatsentimentapi.herokuapp.com/chat/0/list) | chat_id
Get sentiment from messages | GET | [/chat/<chat_id>/sentiment](http://chatsentimentapi.herokuapp.com/chat/0/sentiment) | chat_id
Get user recommendations | GET | [/user/<user_id>/recommend](http://chatsentimentapi.herokuapp.com/user/0/recommend) | user_id
Create a new user | POST | [/user/create](http://chatsentimentapi.herokuapp.com/user/create) | username
Create a new chat | POST | [/chat/create](http://chatsentimentapi.herokuapp.com/chat/create) | users array
Add a user to an existing chat | POST | [/chat/<chat_id>/adduser](http://chatsentimentapi.herokuapp.com/chat/0/adduser) | chat_id, user_id
Add a message to an existing chat | POST | [/chat/<chat_id>/addmessage](http://chatsentimentapi.herokuapp.com/chat/0/addmessage) | chat_id, user, message

