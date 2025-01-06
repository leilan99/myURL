import sqlite3
import threading
import string
import random
from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

DATABASE = 'links.db'
VERBOSE = True

# Setting up database
def setup_database():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              original_url TEXT NOT NULL,
              short_code TEXT UNIQUE NOT NULL
        )
    '''
    )
    conn.commit()
    conn.close()
    return conn

def get_original(short_code):
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None

@app.route("/api/<short_code>")
def redirect_short_url(short_code):
    original_url = get_original(short_code)
    if original_url:
        return redirect(original_url)
    else:
        return jsonify({"error": "Original URL not found."}), 404
    
@app.route("/api/add", methods=['POST'])
def add_url():
    data = request.get_json()

    if not data or 'original_url' not in data:
        return jsonify({"error": "Original URL not found."}), 404
    
    original_url = data['original_url']

    def generate_shortcode(length=5):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    short_code = generate_shortcode()
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    c = conn.cursor()

    while True:
        try:
            c.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
            conn.commit()
            break
        except sqlite3.IntegrityError:
            short_code = generate_shortcode()

    conn.close()
    return jsonify({"short_code": short_code}), 201

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, port=9712)    
