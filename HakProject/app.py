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

@app.route('/api/submit_url', methods=['POST'])
def submit_url():
    url = request.json.get('url')
    if url in data_store:
        return jsonify({'status': 'already_analyzed', 'progress': data_store[url]['progress']})

    headings, paragraphs = analyze_website(url)
    data_store[url] = {
        'headings': headings,
        'paragraphs': paragraphs,
        'progress': '100%'  # Если анализ завершен
    }

    return jsonify({'status': 'analyzed', 'progress': data_store[url]['progress']})

@app.route('/api/ask_question', methods=['POST'])
def ask_question():
    url = request.json.get('url')
    question = request.json.get('question')

    if url not in data_store:
        return jsonify({'error': 'URL not found'})

    paragraphs = data_store[url]['paragraphs']

if __name__ == '__main__':
    app.run(debug=True)