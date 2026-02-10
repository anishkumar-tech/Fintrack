from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float)
    date = Column(Date)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="expenses")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Float)
    next_date = Column(Date)

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, unique=True, index=True) # Format: YYYY-MM
    limit = Column(Float)
