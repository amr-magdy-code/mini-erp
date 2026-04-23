from flask import Flask, render_template, request, redirect
import database
import requests
from datetime import date

app = Flask(__name__)
database.create_tables()

@app.route("/")
def index():
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT orders.id, customers.name, orders.order_date, 
               orders.status, orders.total_price 
        FROM orders 
        JOIN customers ON orders.customer_id = customers.id
    """)
    orders = cursor.fetchall()
    conn.close()
    return render_template("sales.html", orders=orders)

@app.route("/new", methods=["GET", "POST"])
def new_order():
    try:
        response = requests.get("http://localhost:5000/api/products")
        products = response.json()
    except:
        products = []

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        conn = database.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO customers (name, phone, address) 
            VALUES (?, ?, ?)
        """, (name, phone, address))
        customer_id = cursor.lastrowid

        product_ids = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")
        prices = request.form.getlist("unit_price")
        names = request.form.getlist("product_name")

        total = 0
        items = []
        for i in range(len(product_ids)):
            qty = int(quantities[i])
            price = float(prices[i])
            subtotal = qty * price
            total += subtotal
            items.append((product_ids[i], names[i], qty, price))

        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, status, total_price)
            VALUES (?, ?, ?, ?)
        """, (customer_id, str(date.today()), "Pending", total))
        order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, item[0], item[1], item[2], item[3]))

            requests.post("http://localhost:5000/api/update_quantity", json={
                "product_id": item[0],
                "quantity_sold": item[2]
            })

        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("sales.html", show_form=True, products=products)

if __name__ == "__main__":
    app.run(port=5001, debug=True)