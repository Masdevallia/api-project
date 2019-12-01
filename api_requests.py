
# Request examples:

import requests

# Get chat messages:
chat_id = 0
messages = requests.get(f'http://localhost:8080/chat/{chat_id}/list').json()

# Get sentiments from messages:
chat_id = 0
sentiments = requests.get(f'http://localhost:8080/chat/{chat_id}/sentiment').json()

# Add a new user:
newuser = {'username': 'Cristina Rota'}
users = requests.post('http://localhost:8080/user/create', data=newuser).json()

# Add a new chat:
newchat = {'users': '[8, 9, 10]'}
chats = requests.post('http://localhost:8080/chat/create', data=newchat).json()

# Add a user to an existing chat:
chat_id = 1
user = {'userId': 1}
usertochat = requests.post(f'http://localhost:8080/chat/{chat_id}/adduser', data=user).json()

# Add a message to an existing chat:
chat_id = 0
message = {'user':0, 'message':'Moron!'}
newMessage = requests.post(f'http://localhost:8080/chat/{chat_id}/addmessage', data=message).json()