# Mini ERP System

A simple ERP system built with Python and Flask, consisting of two integrated subsystems that communicate with each other.

## Systems

### 1. Inventory System (Port 5000)
- Add and manage products
- Track stock quantities
- Low stock and out of stock alerts
- REST API for inter-system communication

### 2. Sales System (Port 5001)
- Create customer orders
- Automatically updates inventory quantity after each order
- View all orders and statuses

## How They Communicate
The two systems communicate via REST API:
- Sales fetches products from Inventory via `GET /api/products`
- Sales updates stock via `POST /api/update_quantity`

## Technologies Used
- Python 3
- Flask
- SQLite
- HTML & CSS

## How to Run

### 1. Install dependencies

### 2. Run Inventory System

### 3. Run Sales System (open a new terminal)

### 4. Open in Browser
- Inventory System → http://localhost:5000
- Sales System → http://localhost:5001

## Project Structure
mini-erp/
├── inventory_system/
│   ├── app.py
│   ├── database.py
│   └── templates/
│       └── inventory.html
└── sales_system/
├── app.py
├── database.py
└── templates/
└── sales.html
