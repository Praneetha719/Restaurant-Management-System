import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'restaurant.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    # Menu table
    conn.execute('''CREATE TABLE IF NOT EXISTS menu (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL
                    );''')
    
    # Users table
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL CHECK(role IN ('admin', 'cashier'))
                    );''')
    
    # Orders table for billing
    conn.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        total_amount REAL NOT NULL,
                        cashier_id INTEGER,
                        FOREIGN KEY (cashier_id) REFERENCES users(id)
                    );''')
    
    # Order items table
    conn.execute('''CREATE TABLE IF NOT EXISTS order_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        menu_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL,
                        FOREIGN KEY (order_id) REFERENCES orders(id),
                        FOREIGN KEY (menu_id) REFERENCES menu(id)
                    );''')
    
    conn.commit()
    
    # Create default admin user if it doesn't exist
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        admin_password = generate_password_hash('admin123')
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                    ('admin', admin_password, 'admin'))
    
    # Create default cashier user if it doesn't exist
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('cashier',))
    if cursor.fetchone()[0] == 0:
        cashier_password = generate_password_hash('cashier123')
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                    ('cashier', cashier_password, 'cashier'))
    
    conn.commit()
    return conn

if __name__ == '__main__':
    init_db()
    print('Database initialized at', DB_PATH)
    print('Default users created:')
    print('  Admin - username: admin, password: admin123')
    print('  Cashier - username: cashier, password: cashier123')
