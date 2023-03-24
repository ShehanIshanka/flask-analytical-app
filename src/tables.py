from sqlalchemy import Column, DATETIME, DateTime, Float, Integer, VARCHAR
from src.db import Base


class Orders(Base):
    __tablename__ = "orders"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DATETIME)
    vendor_id = Column(Integer)
    customer_id = Column(Integer)


class OrderLines(Base):
    __tablename__ = "order_lines"
    __table_args__ = {"sqlite_autoincrement": True}
    order_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    product_description = Column(VARCHAR(40))
    product_price = Column(Integer)
    product_vat_rate = Column(Float)
    discount_rate = Column(Float)
    quantity = Column(Integer)
    full_price_amount = Column(Integer)
    discounted_amount = Column(Float)
    vat_amount = Column(Float)
    total_amount = Column(Float)


class Products(Base):
    __tablename__ = "products"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(VARCHAR(40))


class Promotions(Base):
    __tablename__ = "promotions"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(VARCHAR(40))


class Product_promotions(Base):
    __tablename__ = "product_promotions"
    __table_args__ = {"sqlite_autoincrement": True}
    date = Column(DateTime)
    product_id = Column(Integer, primary_key=True)
    promotion_id = Column(Integer)


class Commissions(Base):
    __tablename__ = "commissions"
    __table_args__ = {"sqlite_autoincrement": True}
    date = Column(DateTime)
    vendor_id = Column(Integer, primary_key=True)
    rate = Column(Float)
