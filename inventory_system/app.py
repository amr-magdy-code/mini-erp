from flask import Flask, render_template, request, redirect, jsonify
import database

app = Flask(__name__)
database.create_tables()

# عرض كل المنتجات
@app.route("/")
def index():
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("inventory.html", products=products)

# إضافة منتج جديد
@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        reorder_threshold = request.form["reorder_threshold"]

        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, category, price, quantity, reorder_threshold)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, price, quantity, reorder_threshold))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("inventory.html", show_form=True)

# تعديل كمية منتج
@app.route("/update/<int:product_id>", methods=["POST"])
def update_quantity(product_id):
    new_quantity = request.form["quantity"]
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
    conn.commit()
    conn.close()
    return redirect("/")

# API - جيب كل المنتجات
@app.route("/api/products")
def api_products():
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    products = []
    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "price": row[3],
            "quantity": row[4]
        })
    return jsonify(products)

# API - تحديث الكمية لما بيتعمل طلب
@app.route("/api/update_quantity", methods=["POST"])
def api_update_quantity():
    data = request.get_json()
    product_id = data["product_id"]
    quantity_sold = data["quantity_sold"]

    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products 
        SET quantity = quantity - ? 
        WHERE id = ?
    """, (quantity_sold, product_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)