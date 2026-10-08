# 📦 Smart Inventory & Stock Alert System

A full-stack inventory management and stock monitoring system built using **Python, Flask, SQLite, Pandas, JavaScript, and n8n**.

This project allows users to manage products, monitor inventory levels, analyze stock data, and automatically receive Telegram alerts when products reach or fall below their minimum stock level.



## 🚀 Features

- ➕ Add new products
- 📋 View all products
- 👁️ View product details
- ✏️ Update product quantity
- 🗑️ Delete products
- 🔍 Search products
- 🏷️ Filter products by category
- 🟢 Filter normal-stock products
- 🔴 Filter low-stock products
- 🔄 Refresh inventory data
- 📊 Inventory summary dashboard
- 💰 Calculate total inventory value
- ⚠️ Detect low-stock products
- 📱 Responsive frontend
- 📈 Inventory analytics using Pandas
- 🤖 Automated low-stock alerts using n8n
- 📱 Telegram stock notifications
- 🗄️ SQLite database
- 🌐 Flask REST API
- 🔗 Frontend-to-backend API communication



## 📸 Project Screenshots

### 🏠 Inventory Dashboard

The main dashboard provides an overview of products, inventory value, and low-stock products.

![Inventory Dashboard](screenshots/dashboard.png)



### ⚠️ Low Stock Monitoring

The system highlights products that have reached or fallen below their minimum stock level.

![Low Stock Products](screenshots/low-stock.png)



### 🤖 n8n Automation Workflow

The n8n workflow automatically checks low-stock products and sends Telegram notifications.

![n8n Workflow](screenshots/n8n-workflow.png)



## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| Flask | REST API and web server |
| SQLite | Database management |
| Pandas | Inventory data analysis |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend functionality |
| n8n | Workflow automation |
| Telegram | Stock alert notifications |
| Git | Version control |
| GitHub | Source code management |



## 🏗️ Project Architecture


                         User
                           │
                           ▼
                  ┌─────────────────┐
                  │    Frontend     │
                  │   HTML/CSS/JS   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Flask REST    │
                  │       API       │
                  └────────┬────────┘
                           │
                     ┌─────┴─────┐
                     ▼           ▼
              ┌───────────┐  ┌───────────┐
              │  SQLite   │  │  Pandas   │
              │  Database │  │ Analytics │
              └─────┬─────┘  └───────────┘
                    │
                    ▼
               Low Stock Check
                    │
                    ▼
               ┌──────────┐
               │   n8n    │
               │Automation│
               └────┬─────┘
                    │
                    ▼
               ┌──────────┐
               │ Telegram │
               │  Alert   │
               └──────────┘

📁 Project Structure
Smart Inventory & Stock Alert System/
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── database/
│   └── inventory.db
│
├── analytics/
│   └── analytics.py
│
├── n8n/
│   └── workflow.json
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── screenshots/
│
└── README.md

⚙️ How to Run
1. Install Python Dependencies

Install the required Python packages:

pip install flask pandas

Or, if you have a requirements.txt file:

pip install -r backend/requirements.txt
2. Start the Flask Backend

Open a terminal and navigate to the backend folder:

cd backend

Run the Flask application:

python app.py

The server will start at:

http://127.0.0.1:5000
3. Open the Inventory Dashboard

Open the following URL in your browser:

http://127.0.0.1:5000/inventory

The dashboard allows you to:

Add products
View products
Update stock
Delete products
Search products
Filter products
Monitor stock levels
View inventory statistics

📊 Inventory Analytics

The project includes a Pandas-based analytics module for analyzing inventory data.

The analytics module provides:

📦 Inventory value per product
📊 Stock status
⚠️ Low-stock products
💰 Total inventory value
🏷️ Category-wise inventory value
🥇 Highest-value category
Run Analytics

Navigate to the analytics folder:

cd analytics

Run the analytics program:

python analytics.py
🤖 n8n Automation

n8n is used to automate the low-stock alert system.

Automation Workflow
Get Low Stock Products
          │
          ▼
     Check Product
          │
          ▼
  Create Alert Message
          │
          ▼
 Check Existing Alert
          │
          ▼
If Alert Does Not Exist
          │
          ▼
  Send Telegram Alert
          │
          ▼
      Store Alert

The workflow automatically:
Checks products with low stock.
Detects products that have reached their minimum stock level.
Creates a low-stock alert message.
Checks whether an alert already exists.
Sends a Telegram notification.
Stores the alert to prevent duplicate notifications.
📱 Example Telegram Alert

⚠️ LOW STOCK ALERT
Keyboard has only 5 units left.

Minimum stock is 10.
🔌 REST API Endpoints

The Flask backend provides the following REST API endpoints:

Method	Endpoint	Description
GET	/products	Get all products
POST	/products	Add a new product
GET	/products/<id>	Get a specific product
PUT	/products/<id>	Update product information
DELETE	/products/<id>	Delete a product
GET	/products/low-stock	Get low-stock products
GET	/inventory-summary	Get inventory statistics
POST	/alerts	Store a stock alert
GET	/alerts/<product_id>	Get alert information

🗄️ Database
The application uses SQLite to store inventory and alert information.
Products Table
The products table contains:

Product ID
Product Name
Category
Quantity
Minimum Stock
Price
Supplier
Alerts Table

The alerts table contains:

Alert ID
Product ID
Alert Message

📈 Inventory Calculation

The system calculates the inventory value of each product using:

Inventory Value = Quantity × Price
Example
Quantity = 20
Price = ₹1,000

Inventory Value = 20 × ₹1,000

Inventory Value = ₹20,000

⚠️ Low Stock Detection

A product is considered Low Stock when:

Quantity <= Minimum Stock
Example
Quantity = 5
Minimum Stock = 10

5 <= 10

Status = Low Stock
🔄 CRUD Operations

The application supports complete product management through CRUD operations.

Create

Add a new product using the frontend or REST API.

Read

View all products or retrieve a specific product.

Update

Update product information such as quantity or category.

Delete

Remove a product from the inventory.

🎯 Future Improvements

The following features can be added in future versions:

🔐 API authentication
👤 User authentication and login
📊 Interactive inventory charts
📈 Advanced inventory analytics
📧 Email stock alerts
🔄 Automatic alert reset after restocking
☁️ Cloud deployment
📱 Improved mobile interface
🔎 Advanced product search
📦 Supplier management
📋 Inventory transaction history
📊 Inventory dashboard charts
🎓 Learning Outcomes

This project demonstrates practical experience with:

Python programming
Flask REST API development
CRUD operations
SQLite database management
SQL queries
Pandas data analysis
HTML, CSS, and JavaScript
REST API communication
n8n workflow automation
Telegram bot integration
Git and GitHub
Full-stack project development
Workflow automation

👨‍💻 Author
Om Patel

Python Backend & Automation Developer
This project was built to demonstrate practical skills in:
Python → Flask → REST API → SQLite → Pandas → JavaScript → n8n → Telegram

⭐ Project Goal

The goal of this project is to build a practical real-world inventory management system that combines:

Backend development
REST API development
Database management
Data analysis
Frontend development
Workflow automation
Automated stock notifications

into a single full-stack application.

📌 Project Status
Status: ✅ Completed
More features and improvements may be added in future versions.