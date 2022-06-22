import requests


url = "http://127.0.0.1:5000/repos"


response = requests.get(url)

response_data = response.json()

for s in response_data:
    print(s)

