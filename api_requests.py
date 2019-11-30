
# Request examples:

import requests

chat_id = 0
messages = requests.get(f'http://localhost:8080/chat/{chat_id}/list').json()
sentiments = requests.get(f'http://localhost:8080/chat/{chat_id}/sentiment').json()

newuser = {'username': 'Cristina Rota'}
users = requests.post('http://localhost:8080/user/create', data=newuser).json()

newchat = {'users': '[8, 9, 10]'}
chats = requests.post('http://localhost:8080/chat/create', data=newchat).json()

