from ..data.dependency import Base
from sqlalchemy import Column, Integer, String, Text, Numeric, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String, nullable=False)
    supplier_address = Column(Text, nullable=False)
    supplier_phonenumber = Column(Numeric, nullable=False)

    items = relationship("Item", back_populates="supplier")
    item_warehouse = relationship("ItemWarehouse", back_populates="supplier")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)

    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    item_price = Column(Float, nullable=False)
    item_count = Column(Integer, nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    supplier = relationship("Supplier", back_populates="items")
    category = relationship("Category", back_populates="items")
    transactions = relationship("Transaction", back_populates="item")
    selling = relationship("Selling", back_populates="item", uselist=False)
    item_warehouse = relationship("ItemWarehouse", back_populates="item", uselist=False)


class Selling(Base):
    __tablename__ = "selling"

    id = Column(Integer, primary_key=True, index=True)
    selling_price = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)

    item = relationship("Item", back_populates="selling")


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    sold_to = Column(String, nullable=False)
    sold_amount = Column(Integer, nullable=False)
    sold_date = Column(DateTime, default=func.now())
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)

    item = relationship("Item", back_populates="transactions")


class ItemWarehouse(Base):
    __tablename__="item_warehouse"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    current_amount = Column(Integer, nullable=False)

    item = relationship("Item", back_populates="item_warehouse")
    supplier = relationship("Supplier", back_populates="item_warehouse")
