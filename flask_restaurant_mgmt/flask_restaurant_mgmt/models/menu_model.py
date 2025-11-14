# Simple model helpers (optional)
import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__ + '/../'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'restaurant.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
