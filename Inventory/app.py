from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace these values with your MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Exynox7510#',
    'database': 'inventory'
}

@app.route('/')
def index():
    # Fetch all products from the database
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
