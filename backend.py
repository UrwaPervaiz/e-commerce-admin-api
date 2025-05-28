from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import random

DATABASE_URL = "sqlite:///./ecommerce.db"
database_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
database_session = sessionmaker(bind=database_engine)
Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    product_category = Column(String)
    product_price = Column(Float)
    product_stock = Column(Integer)

class SaleModel(Base):
    __tablename__ = "sales"
    sale_id = Column(Integer, primary_key=True, index=True)
    sold_product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity_sold = Column(Integer)
    date_of_sale = Column(DateTime)
    related_product = relationship("ProductModel")

Base.metadata.create_all(bind=database_engine)

app = FastAPI()

class ProductInput(BaseModel):
    product_name: str
    product_category: str
    product_price: float
    product_stock: int

class StockUpdate(BaseModel):
    product_stock: int

@app.post("/products/")
def register_product(product_data: ProductInput):
    session = database_session()
    new_product_entry = ProductModel(**product_data.dict())
    session.add(new_product_entry)
    session.commit()
    session.refresh(new_product_entry)
    session.close()
    return new_product_entry

@app.get("/inventory/")
def fetch_inventory(threshold: Optional[int] = None):
    session = database_session()
    if threshold is not None:
        product_list = session.query(ProductModel).filter(ProductModel.product_stock <= threshold).all()
    else:
        product_list = session.query(ProductModel).all()
    session.close()
    return product_list

@app.put("/inventory/{product_id}")
def modify_inventory(product_id: int, stock_details: StockUpdate):
    session = database_session()
    target_product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not target_product:
        session.close()
        raise HTTPException(status_code=404, detail="Product not found")
    target_product.product_stock = stock_details.product_stock
    session.commit()
    session.refresh(target_product)
    session.close()
    return target_product

@app.get("/sales/")
def fetch_sales(from_date: Optional[datetime] = None, to_date: Optional[datetime] = None, item_id: Optional[int] = None, category_filter: Optional[str] = None):
    session = database_session()
    sales_query = session.query(SaleModel)
    if from_date:
        sales_query = sales_query.filter(SaleModel.date_of_sale >= from_date)
    if to_date:
        sales_query = sales_query.filter(SaleModel.date_of_sale <= to_date)
    if item_id:
        sales_query = sales_query.filter(SaleModel.sold_product_id == item_id)
    if category_filter:
        sales_query = sales_query.join(ProductModel).filter(ProductModel.product_category == category_filter)
    sales_records = sales_query.all()
    session.close()
    return sales_records

@app.get("/revenue/")
def calculate_revenue(timeframe: str = Query("daily", enum=["daily", "weekly", "monthly", "yearly"])):
    session = database_session()
    current_time = datetime.now()
    if timeframe == "daily":
        beginning_date = current_time - timedelta(days=1)
    elif timeframe == "weekly":
        beginning_date = current_time - timedelta(weeks=1)
    elif timeframe == "monthly":
        beginning_date = current_time - timedelta(days=30)
    elif timeframe == "yearly":
        beginning_date = current_time - timedelta(days=365)
    revenue_sales = session.query(SaleModel).filter(SaleModel.date_of_sale >= beginning_date).all()
    total_earnings = sum(sale.quantity_sold * sale.related_product.product_price for sale in revenue_sales)
    session.close()
    return {"timeframe": timeframe, "revenue": total_earnings}

@app.post("/populate-demo/")
def generate_sample_data():
    session = database_session()
    session.query(SaleModel).delete()
    session.query(ProductModel).delete()
    category_choices = ["Electronics", "Books", "Clothing"]
    for index in range(10):
        mock_product = ProductModel(
            product_name=f"Product {index+1}",
            product_category=random.choice(category_choices),
            product_price=round(random.uniform(10.0, 500.0), 2),
            product_stock=random.randint(5, 100)
        )
        session.add(mock_product)
        session.commit()
        session.refresh(mock_product)
        for _ in range(random.randint(5, 20)):
            mock_sale = SaleModel(
                sold_product_id=mock_product.product_id,
                quantity_sold=random.randint(1, 5),
                date_of_sale=datetime.now() - timedelta(days=random.randint(0, 60))
            )
            session.add(mock_sale)
    session.commit()
    session.close()
    return {"message": "Demo data populated"}
