from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
from datetime import datetime
import stripe

app = Flask(__name__)
app.secret_key = 'ecommerce-secret-key-2024'

stripe.api_key = 'sk_test_demo'
STRIPE_PUBLISHABLE_KEY = 'pk_test_demo'

class Database:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                image_url TEXT,
                stock INTEGER DEFAULT 0,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_amount DECIMAL(10, 2),
                status TEXT DEFAULT 'pending',
                stripe_payment_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price DECIMAL(10, 2),
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        self.populate_sample_products(cursor)
        
        conn.commit()
        conn.close()
    
    def populate_sample_products(self, cursor):
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            products = [
                ('Wireless Headphones', 'Premium bluetooth headphones with noise cancellation', 199.99, '/static/images/headphones.svg', 50, 'Electronics'),
                ('Laptop Stand', 'Adjustable aluminum laptop stand for better ergonomics', 79.99, '/static/images/laptop-stand.svg', 30, 'Accessories'),
                ('Coffee Mug', 'Ceramic coffee mug with heat retention technology', 24.99, '/static/images/coffee-mug.svg', 100, 'Home'),
                ('Gaming Mouse', 'High-precision gaming mouse with RGB lighting', 89.99, '/static/images/gaming-mouse.svg', 25, 'Electronics'),
                ('Desk Lamp', 'LED desk lamp with adjustable brightness and color', 59.99, '/static/images/desk-lamp.svg', 40, 'Home'),
                ('Phone Case', 'Protective phone case with drop protection', 29.99, '/static/images/phone-case.svg', 75, 'Accessories'),
                ('Bluetooth Speaker', 'Portable waterproof bluetooth speaker', 149.99, '/static/images/bluetooth-speaker.svg', 35, 'Electronics'),
                ('Notebook', 'Premium lined notebook with leather cover', 34.99, '/static/images/notebook.svg', 60, 'Office')
            ]
            
            cursor.executemany('INSERT INTO products (name, description, price, image_url, stock, category) VALUES (?, ?, ?, ?, ?, ?)', products)

    def get_connection(self):
        return sqlite3.connect('ecommerce.db')

db = Database()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_cart_total():
    if 'cart' not in session:
        return 0, 0
    
    total = 0
    item_count = 0
    conn = db.get_connection()
    cursor = conn.cursor()
    
    for product_id, quantity in session['cart'].items():
        cursor.execute('SELECT price FROM products WHERE id = ?', (product_id,))
        result = cursor.fetchone()
        if result:
            total += result[0] * quantity
            item_count += quantity
    
    conn.close()
    return total, item_count

@app.context_processor
def inject_cart_info():
    total, count = get_cart_total()
    return dict(cart_total=total, cart_count=count)

@app.route('/')
def index():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
    products = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, hash_password(password)))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username FROM users WHERE username = ? AND password_hash = ?', 
                      (username, hash_password(password)))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', cart_items=[], total=0)
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cart_items = []
    total = 0
    
    for product_id, quantity in session['cart'].items():
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        if product:
            item_total = product[3] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if quantity > 0:
        session['cart'][str(product_id)] = quantity
        flash('Cart updated!', 'success')
    else:
        if str(product_id) in session['cart']:
            del session['cart'][str(product_id)]
        flash('Product removed from cart!', 'info')
    
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    if 'cart' in session and str(product_id) in session['cart']:
        del session['cart'][str(product_id)]
        session.modified = True
    flash('Product removed from cart!', 'info')
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash('Please login to checkout.', 'error')
        return redirect(url_for('login'))
    
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('view_cart'))
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    user_email = user[0] if user else ''
    conn.close()
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cart_items = []
    cart_total = 0
    
    for product_id, quantity in session['cart'].items():
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        if product:
            item_total = product[3] * quantity
            cart_items.append({
                'name': product[1],
                'price': product[3],
                'quantity': quantity
            })
            cart_total += item_total
    
    conn.close()
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         cart_total=cart_total,
                         user_email=user_email,
                         stripe_publishable_key=STRIPE_PUBLISHABLE_KEY)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'user_id' not in session:
        flash('Please login to complete your order.', 'error')
        return redirect(url_for('login'))
    
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('view_cart'))
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        total = 0
        for product_id, quantity in session['cart'].items():
            cursor.execute('SELECT price FROM products WHERE id = ?', (product_id,))
            price_result = cursor.fetchone()
            if price_result:
                total += price_result[0] * quantity
        
        cursor.execute('INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)', 
                      (session['user_id'], total, 'completed'))
        order_id = cursor.lastrowid
        
        for product_id, quantity in session['cart'].items():
            cursor.execute('SELECT price, stock FROM products WHERE id = ?', (product_id,))
            product_data = cursor.fetchone()
            
            if product_data:
                price, current_stock = product_data
                cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                              (order_id, product_id, quantity, price))
                new_stock = max(0, current_stock - quantity)
                cursor.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))
        
        conn.commit()
        conn.close()
        
        session.pop('cart', None)
        session.modified = True
        
        flash('Order completed successfully!', 'success')
        return redirect(url_for('payment_success', order_id=order_id, total=total))
        
    except Exception as e:
        flash(f'Error processing order: {str(e)}', 'error')
        return redirect(url_for('checkout'))

@app.route('/payment_success')
def payment_success():
    order_id = request.args.get('order_id', 'N/A')
    total_amount = request.args.get('total', 0)
    return render_template('payment_success.html', 
                         order_id=order_id, 
                         total_amount=float(total_amount))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('Please login to view orders.', 'error')
        return redirect(url_for('login'))
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, total_amount, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],))
    orders_data = cursor.fetchall()
    orders_list = []
    
    for order_row in orders_data:
        order_id, total_amount, status, created_at = order_row
        
        cursor.execute('''
            SELECT oi.quantity, oi.price, p.name, p.image_url
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        
        items_data = cursor.fetchall()
        order_items_list = []
        
        for item_row in items_data:
            quantity, price, product_name, image_url = item_row
            item_dict = {
                'quantity': quantity,
                'price': price,
                'product': {'name': product_name, 'image_url': image_url}
            }
            order_items_list.append(item_dict)
        
        try:
            created_at_dt = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        except:
            created_at_dt = datetime.now()
        
        order_dict = {
            'id': order_id,
            'total_amount': total_amount,
            'status': status,
            'created_at': created_at_dt,
            'order_items': order_items_list
        }
        orders_list.append(order_dict)
    
    conn.close()
    return render_template('orders.html', orders=orders_list)

if __name__ == '__main__':
    app.run(debug=True)
