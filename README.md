E-commerce Admin API
Welcome
This project is a beginner-friendly backend API built for an E-commerce Admin Dashboard. It helps store managers track sales, revenue, inventory, and register new products.
Tech Stack
- Language: Python
- Framework: FastAPI
- API Type: RESTful
- Database: SQLite (can switch to PostgreSQL/MySQL)
- Extras: SQLAlchemy ORM, Uvicorn server
Getting Started
1. Clone the repository:
   git clone https://github.com/UrwaPervaiz/ecommerce-admin-api.git
   cd ecommerce-admin-api

2. Create and activate a virtual environment (Windows):
   python -m venv venv
   venv\Scripts\activate

3. Install the necessary libraries:
   pip install -r requirements.txt
   (or install manually: pip install fastapi uvicorn sqlalchemy psycopg2-binary)

4. Launch the API:
   uvicorn main:app --reload

Access the documentation at:
   - Swagger UI: http://127.0.0.1:8000/docs
   - Redoc: http://127.0.0.1:8000/redoc
Database Structure
- Products: Details about each product
- Sales: Tracks when and what was sold
- Inventory: Manages available stock
- Categories: Groups of similar products

To try with sample data, run:
   python populate_demo.py
API Endpoints
Sales Insights
- GET /sales/ → Get sales by date range
- GET /sales/filter → Filter by product/category/date
- GET /revenue/daily → Daily revenue summary

Inventory Management
- GET /inventory/ → Check current inventory
- PUT /inventory/update → Update stock quantity
- GET /inventory/low-stock → See low stock items

Product Management
- POST /products/ → Add a new product
Testing with Demo Data
Run:
   python populate_demo.py
This will insert sample data like products on Amazon & Walmart.
License
MIT License — free for personal and commercial use.
Contact
Got questions or ideas? Reach out to yourname@domain.com
Database Documentation
This project uses a relational database schema (SQLite by default, with options to switch to PostgreSQL or MySQL).

Tables and Their Purposes:
- Products: Stores information about each product such as name, price, category, description, and stock quantity.
- Sales: Records each sale transaction, including the product sold, quantity, sale amount, and timestamp.
- Inventory: Tracks the current stock status of each product, historical stock changes, and generates low stock alerts.
- Categories: Helps group products logically (e.g., Electronics, Clothing, etc.) for better sales insights and filtering.

Relationships Between Entities:
- One-to-many relationship between `Categories` and `Products`: Each category can have multiple products.
- One-to-many relationship between `Products` and `Sales`: A product can appear in multiple sales.
- One-to-one or one-to-many between `Products` and `Inventory`: Inventory keeps stock information for each product.

These relationships are used to join data efficiently for generating reports, filtering by category, and tracking inventory levels.
