from flask import Flask, jsonify , request , render_template
import sqlite3
import os

app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend",
    static_url_path=""
)

# Database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "database", "inventory.db")


# Create products table
def create_table():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            minimum_stock INTEGER NOT NULL,
            price REAL NOT NULL,
            supplier TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            alert_message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():

    return jsonify({
        "message": "Smart Inventory API is running 🚀"
    })

#add product
@app.route("/products", methods=["POST"])
def add_product():

    data = request.get_json()

    required_fields = [
        "product_name",
        "category",
        "quantity",
        "minimum_stock",
        "price",
        "supplier"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "message": f"Missing field: {field}"
            }), 400

    for field in required_fields:
        if data[field] == "":
            return jsonify({
                "message": f"{field} cannot be empty"
            }), 400

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products
        (product_name, category, quantity, minimum_stock, price, supplier)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["product_name"],
        data["category"],
        data["quantity"],
        data["minimum_stock"],
        data["price"],
        data["supplier"]
    ))

    connection.commit()

    product_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Product added successfully",
        "product_id": product_id
    }), 201

#get product
@app.route("/products", methods=["GET"])
def get_products():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    connection.close()

    product_list = []

    for product in products:
        product_list.append({
            "id": product[0],
            "product_name": product[1],
            "category": product[2],
            "quantity": product[3],
            "minimum_stock": product[4],
            "price": product[5],
            "supplier": product[6]
        })

    return jsonify(product_list)

#low stock
@app.route("/products/low-stock", methods=["GET"])
def low_stock():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE quantity <= minimum_stock
    """)

    products = cursor.fetchall()

    connection.close()

    product_list = []

    for product in products:
        product_list.append({
            "id": product[0],
            "product_name": product[1],
            "category": product[2],
            "quantity": product[3],
            "minimum_stock": product[4],
            "price": product[5],
            "supplier": product[6]
        })

    return jsonify(product_list)

#update product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if "quantity" in data:

        cursor.execute("""
            UPDATE products
            SET quantity = ?
            WHERE id = ?
        """, (
            data["quantity"],
            product_id
        ))

    elif "category" in data:

        cursor.execute("""
            UPDATE products
            SET category = ?
            WHERE id = ?
        """, (
            data["category"],
            product_id
        ))

    connection.commit()

    connection.close()

    return jsonify({
        "message": "Product updated successfully"
    })
#delete product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    connection.commit()

    connection.close()

    return jsonify({
        "message": "Product deleted successfully"
    })

#get product id
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE id = ?
    """, (product_id,))

    product = cursor.fetchone()

    connection.close()

    if product is None:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify({
        "id": product[0],
        "product_name": product[1],
        "category": product[2],
        "quantity": product[3],
        "minimum_stock": product[4],
        "price": product[5],
        "supplier": product[6]
    })

@app.route("/inventory-summary", methods=["GET"])
def inventory_summary():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("""
        SELECT SUM(quantity * price)
        FROM products
    """)
    total_inventory_value = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE quantity <= minimum_stock
    """)
    low_stock_products = cursor.fetchone()[0]

    connection.close()

    return jsonify({
        "total_products": total_products,
        "total_inventory_value": total_inventory_value,
        "low_stock_products": low_stock_products
    })

@app.route("/alerts", methods=["POST"])
def save_alert():

    data = request.get_json()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts
        (product_id, alert_message)
        VALUES (?, ?)
    """, (
        data["product_id"],
        data["alert_message"]
    ))

    connection.commit()

    connection.close()

    return jsonify({
        "message": "Alert saved successfully"
    }), 201


@app.route("/alerts/<int:product_id>", methods=["GET"])
def check_alert(product_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM alerts
        WHERE product_id = ?
    """, (product_id,))

    alert = cursor.fetchone()

    connection.close()

    if alert:
        return jsonify({
            "alert_exists": True
        })

    return jsonify({
        "alert_exists": False
    })

@app.route("/inventory")
def inventory_page():
    return render_template("index.html")

if __name__ == "__main__":
    create_table()
    app.run()