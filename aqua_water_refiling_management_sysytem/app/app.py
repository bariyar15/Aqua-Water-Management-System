

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sg155@1505'
app.config['MYSQL_DB'] = 'aqua_water_refiling_management_system'
app.secret_key = 'your_secret_key'  

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user[0], user[1], user[2], user[3])  # Adjust based on your User model
    return None


def create_user(username, password, role):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                   (username, password, role))  # Password is not hashed anymore
    mysql.connection.commit()
    cursor.close()

def get_user(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_all_customers():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    cursor.close()
    return customers

def create_customer(data):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO customer (first_name, middle_name, last_name, email, phone_number, customer_type, balance, address) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                   (data['first_name'], data['middle_name'], data['last_name'], data['email'], data['phone_number'], 
                    data['customer_type'], data['balance'], data['address']))
    mysql.connection.commit()
    cursor.close()

def get_all_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    cursor.close()
    return products

def create_product(data):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO product (product_name, price_per_unit, stock_quantity) VALUES (%s, %s, %s)", 
                   (data['product_name'], data['price_per_unit'], data['stock_quantity']))
    mysql.connection.commit()
    cursor.close()

def get_all_orders():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM orderDetails")
    orders = cursor.fetchall()
    cursor.close()
    return orders

def create_order(data):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO orderDetails (customerID, orderDate, deliveryDate, amount, orderStatus) "
                   "VALUES (%s, %s, %s, %s, %s)", 
                   (data['customerID'], data['orderDate'], data['deliveryDate'], data['amount'], data['orderStatus']))
    mysql.connection.commit()
    cursor.close()

def get_all_deliveries():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM delivery")
    deliveries = cursor.fetchall()
    cursor.close()
    return deliveries

def create_delivery(data):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO delivery (order_ID, del_date, del_status, delivery_personID) "
                   "VALUES (%s, %s, %s, %s)", 
                   (data['order_ID'], data['del_date'], data['del_status'], data['delivery_personID']))
    mysql.connection.commit()
    cursor.close()

def get_all_payments():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM payment")
    payments = cursor.fetchall()
    cursor.close()
    return payments

def create_payment(data):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO payment (order_id, payment_date, amount_paid, method, status) "
                   "VALUES (%s, %s, %s, %s, %s)", 
                   (data['order_id'], data['payment_date'], data['amount_paid'], data['method'], data['status']))
    mysql.connection.commit()
    cursor.close()

def get_all_suppliers():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM supplier")
    suppliers = cursor.fetchall()
    cursor.close()
    return suppliers

def create_supplier(data):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO supplier (name, contact_number, email, address, supplied_product_ID) "
                   "VALUES (%s, %s, %s, %s, %s)", 
                   (data['name'], data['contact_number'], data['email'], data['address'], data['supplied_product_ID']))
    mysql.connection.commit()
    cursor.close()

def get_all_inventory():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    cursor.close()
    return inventory

def create_inventory(data):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO inventory (product_ID, quantity_available, reorder_level, last_updated) "
                   "VALUES (%s, %s, %s, %s)", 
                   (data['product_ID'], data['quantity_available'], data['reorder_level'], data['last_updated']))
    mysql.connection.commit()
    cursor.close()

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = get_user(username)
        if user_data and user_data[2] == password:  # Assuming password is the third column
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])  # Adjust index as necessary
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check your username and password.')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/customers')
@login_required
def customers():
    all_customers = get_all_customers()
    return render_template('customers.html', customers=all_customers)

@app.route('/customer/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        customer_data = request.form.to_dict()
        create_customer(customer_data)
        return redirect(url_for('customers'))
    return render_template('customer_form.html')

@app.route('/products')
@login_required
def products():
    all_products = get_all_products()
    return render_template('products.html', products=all_products)

@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        product_data = request.form.to_dict()
        create_product(product_data)
        return redirect(url_for('products'))
    return render_template('product_form.html')

@app.route('/orders')
@login_required
def orders():
    all_orders = get_all_orders()
    return render_template('orders.html', orders=all_orders)

@app.route('/order/add', methods=['GET', 'POST'])
@login_required
def add_order():
    if request.method == 'POST':
        order_data = request.form.to_dict()
        create_order(order_data)
        return redirect(url_for('orders'))
    return render_template('order_form.html')

@app.route('/deliveries')
@login_required
def deliveries():
    all_deliveries = get_all_deliveries()
    return render_template('deliveries.html', deliveries=all_deliveries)

@app.route('/delivery/add', methods=['GET', 'POST'])
@login_required
def add_delivery():
    if request.method == 'POST':
        delivery_data = request.form.to_dict()
        create_delivery(delivery_data)
        return redirect(url_for('deliveries'))
    return render_template('delivery_form.html')

@app.route('/payments')
@login_required
def payments():
    all_payments = get_all_payments()
    return render_template('payments.html', payments=all_payments)

@app.route('/payment/add', methods=['GET', 'POST'])
@login_required
def add_payment():
    if request.method == 'POST':
        payment_data = request.form.to_dict()
        create_payment(payment_data)
        return redirect(url_for('payments'))
    return render_template('payment_form.html')

@app.route('/suppliers')
@login_required
def suppliers():
    all_suppliers = get_all_suppliers()
    return render_template('suppliers.html', suppliers=all_suppliers)

@app.route('/supplier/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        supplier_data = request.form.to_dict()
        create_supplier(supplier_data)
        return redirect(url_for('suppliers'))
    return render_template('supplier_form.html')

@app.route('/inventory')
@login_required
def inventory():
    all_inventory = get_all_inventory()
    return render_template('inventory.html', inventory=all_inventory)

@app.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_inventory():
    if request.method == 'POST':
        inventory_data = request.form.to_dict()
        create_inventory(inventory_data)
        return redirect(url_for('inventory'))
    return render_template('inventory_form.html')

if __name__ == '__main__':
    app.run(debug=True)
