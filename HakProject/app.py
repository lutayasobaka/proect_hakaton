from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

data_store = {}

def analyze_website(url, query):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = [p.get_text() for p in soup.find_all('p')]

    # Поиск всех элементов, содержащих запрос
    results = [text for text in paragraphs if query.lower() in text.lower()]

    return results

# Запрос ввода от пользователя
url_input = input("Введите URL сайта (например, https://example.com): ")
query_input = input("Введите ваш запрос для поиска на сайте: ")

# Вызов функции и вывод результатов
found_items = analyze_website(url_input, query_input)
for item in found_items:
    print(item)

if __name__ == '__main__':
    app.run(debug=True)