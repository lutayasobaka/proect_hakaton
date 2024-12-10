from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

    # Загрузка NLP модели (простой подход)
    nltk.download('punkt')
    tokens = word_tokenize(question)

    # Применение TF-IDF для нахождения наиболее релевантного текста
    vectorizer = TfidfVectorizer().fit_transform(paragraphs + [' '.join(tokens)])
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[-1].reshape(1, -1), vectors[:-1])
    best_match_index = cosine_similarities.argsort()[0][-1]

    # Получаем лучший абзац
    best_paragraph = paragraphs[best_match_index]

    # Извлечение первых двух предложений
    sentences = sent_tokenize(best_paragraph)
    short_answer = ' '.join(sentences[:2])  # Берем два первых предложения

    # Вернем результат с предложением
    return jsonify({
        'answer': short_answer,
        'source': data_store[url]['headings'][best_match_index]
    })

if __name__ == '__main__':
    app.run(debug=True)