from flask import Flask, request, jsonify, render_template
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

@app.route('/')
def index():
    return render_template('analyze.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    query = data.get('query')

    # Вызов функции и вывод результатов
    found_items = analyze_website(url, query)

    return jsonify(found_items)

if __name__ == '__main__':
    app.run(debug=True)