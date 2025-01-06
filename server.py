import sqlite3
import threading
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

@app.route("/<short_code>")
def redirect_short_url(short_code):
    original_url = get_original(short_code)
    if original_url:
        return redirect(original_url)
    else:
        return jsonify({"error": "Original URL not found."}), 404

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, port=6600)    
