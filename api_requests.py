
import requests

chat_id = 0
messages = requests.get(f'http://localhost:8080/chat/{chat_id}/list').json()
sentiments = requests.get(f'http://localhost:8080/chat/{chat_id}/sentiment').json()
