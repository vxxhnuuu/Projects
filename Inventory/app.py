from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "sk"  # Change this to a random, secure value

# MySQL configurations
db_config = {
    'user': 'root',
    'password': 'Exynox7510#',
    'host': 'localhost',
    'database': 'inventory',
}

def connect():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = connect()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and password == user[2]:  # Compare passwords directly (not recommended in production)
            session['username'] = username
            session['role'] = user[3]
            return redirect(url_for('index'))
        else:
            return "Login failed. Check your username and password."
    else:
        return "Unable to connect to the database."

@app.route('/index')
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    connection.close()
    
    return render_template('index.html', products=products)


    

@app.route('/add', methods=['POST'])
def add_product():
    # Insert a new product into the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    name = request.form['name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    connection.commit()
    connection.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    # Delete a product from the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    connection.close()
    
    return redirect(url_for('index'))

@app.route('/update/<int:product_id>', methods=['POST'])
def update_product(product_id):
    # Update a product in the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    cursor.execute("UPDATE products SET quantity = %s, price = %s WHERE id = %s", (quantity, price, product_id))
    connection.commit()
    connection.close()
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
