import requests

BASE = "http://127.0.0.1:2024/"

response = requests.get(BASE + "helloworld")
print(response.json())