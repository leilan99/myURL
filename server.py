import sqlite3
import threading
from flask import Flask, jsonify, request

DATABASE = 'links.db'
VERBOSE = True

# Setting up database
def setup_database():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS url_shortner (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              original_url TEXT NOT NULL,
              short_code TEXT UNIQUE NOT NULL
        )
    '''
    )
    conn.commit()
    return conn

