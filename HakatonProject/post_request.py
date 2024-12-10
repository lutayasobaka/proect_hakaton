import requests

url = 'http://127.0.0.1:5000/analyze'
data = {
    "url": "https://ru.wikipedia.org/wiki/Пегас",
    "query": "Происхождение термина"
}

response = requests.post(url, json=data)

print(response.json())

