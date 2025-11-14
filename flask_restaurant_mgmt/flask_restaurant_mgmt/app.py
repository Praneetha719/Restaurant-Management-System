from flask import Flask, render_template, request, redirect, url_for, g, session, flash, jsonify
import sqlite3
import os
from werkzeug.security import check_password_hash
from functools import wraps
from database import init_db

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-change-this-in-production'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'restaurant.db')

# Initialize database on startup
init_db()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' in session:
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    user = get_current_user()
    return render_template('index.html', user=user)

@app.route('/menu')
@login_required
def menu():
    db = get_db()
    items = db.execute('SELECT * FROM menu ORDER BY name').fetchall()
    user = get_current_user()
    return render_template('menu.html', items=items, user=user)

@app.route('/add_item', methods=['GET', 'POST'])
@admin_required
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        db = get_db()
        db.execute('INSERT INTO menu (name, price) VALUES (?, ?)', (name, price))
        db.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('menu'))
    return render_template('add_item.html')

@app.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
@admin_required
def update_item(item_id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        db.execute('UPDATE menu SET name=?, price=? WHERE id=?', (name, price, item_id))
        db.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('menu'))
    item = db.execute('SELECT * FROM menu WHERE id=?', (item_id,)).fetchone()
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('menu'))
    return render_template('update_item.html', item=item)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
@admin_required
def delete_item(item_id):
    db = get_db()
    db.execute('DELETE FROM menu WHERE id=?', (item_id,))
    db.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('menu'))

@app.route('/billing')
@login_required
def billing():
    db = get_db()
    items = db.execute('SELECT * FROM menu ORDER BY name').fetchall()
    user = get_current_user()
    return render_template('billing.html', items=items, user=user)

@app.route('/create_order', methods=['POST'])
@login_required
def create_order():
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({'success': False, 'message': 'No items selected'}), 400
        
        db = get_db()
        total_amount = 0
        
        # Calculate total
        for item in items:
            menu_item = db.execute('SELECT price FROM menu WHERE id = ?', (item['id'],)).fetchone()
            if menu_item:
                total_amount += menu_item['price'] * item['quantity']
        
        # Create order
        cursor = db.cursor()
        cursor.execute('INSERT INTO orders (total_amount, cashier_id) VALUES (?, ?)',
                      (total_amount, session['user_id']))
        order_id = cursor.lastrowid
        
        # Create order items
        for item in items:
            menu_item = db.execute('SELECT price FROM menu WHERE id = ?', (item['id'],)).fetchone()
            if menu_item:
                cursor.execute('INSERT INTO order_items (order_id, menu_id, quantity, price) VALUES (?, ?, ?, ?)',
                              (order_id, item['id'], item['quantity'], menu_item['price']))
        
        db.commit()
        return jsonify({'success': True, 'order_id': order_id, 'total': total_amount})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/orders')
@login_required
def orders():
    db = get_db()
    user = get_current_user()
    
    if user['role'] == 'admin':
        # Admin can see all orders
        orders_list = db.execute('''
            SELECT o.*, u.username as cashier_name 
            FROM orders o 
            LEFT JOIN users u ON o.cashier_id = u.id 
            ORDER BY o.order_date DESC
        ''').fetchall()
    else:
        # Cashier can only see their own orders
        orders_list = db.execute('''
            SELECT o.*, u.username as cashier_name 
            FROM orders o 
            LEFT JOIN users u ON o.cashier_id = u.id 
            WHERE o.cashier_id = ?
            ORDER BY o.order_date DESC
        ''', (session['user_id'],)).fetchall()
    
    # Get order items for each order
    orders_with_items = []
    for order in orders_list:
        items = db.execute('''
            SELECT oi.*, m.name as item_name 
            FROM order_items oi 
            JOIN menu m ON oi.menu_id = m.id 
            WHERE oi.order_id = ?
        ''', (order['id'],)).fetchall()
        orders_with_items.append({
            'order': order,
            'order_items': items
        })
    
    return render_template('orders.html', orders_with_items=orders_with_items, user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
