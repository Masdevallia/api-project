
import requests

chat_id = 0
data = requests.get(f'http://localhost:8080/chat/{chat_id}/list').json()
newdata = requests.get(f'http://localhost:8080/chat/{chat_id}/sentiment').json()
