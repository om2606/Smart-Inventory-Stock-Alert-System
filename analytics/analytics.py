import sqlite3
import pandas as pd

DATABASE = r"C:\Users\omnad\Desktop\Python notes\Daily challenges\n8n project\Smart Inventory & Stock Alert System\database\inventory.db"

connection = sqlite3.connect(DATABASE)

query = "SELECT * FROM products"

df = pd.read_sql_query(query, connection)

connection.close()

print(df)

df["inventory_value"] = df["quantity"] * df["price"]

print("\n=== INVENTORY VALUE ===")
print(df[["product_name", "quantity", "price", "inventory_value"]])

df["stock_status"] = df.apply(
    lambda row: "Low Stock"
    if row["quantity"] <= row["minimum_stock"]
    else "Normal Stock",
    axis=1
)

print("\n=== STOCK STATUS ===")
print(df[["product_name", "quantity", "minimum_stock", "stock_status"]])

low_stock_products = df[df["stock_status"] == "Low Stock"]

print("\n=== LOW STOCK PRODUCTS ===")
print(low_stock_products[
    ["product_name", "quantity", "minimum_stock", "stock_status"]
])

total_inventory_value = df["inventory_value"].sum()

print("\n=== TOTAL INVENTORY VALUE ===")
print("Total Inventory Value: ₹", total_inventory_value)

category_summary = df.groupby("category")["inventory_value"].sum()

print("\n=== CATEGORY-WISE INVENTORY VALUE ===")
print(category_summary)

highest_category = category_summary.idxmax()
highest_value = category_summary.max()

print("\n=== HIGHEST VALUE CATEGORY ===")
print("Category:", highest_category)
print("Inventory Value: ₹", highest_value)