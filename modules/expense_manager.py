from datetime import datetime
from sqlalchemy.orm import Session
from models import Expense, Category

def add_expense(db: Session, title: str, amount: float, date_str: str, category_name: str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    
    # Check if category exists, else create it
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
    
    new_expense = Expense(title=title, amount=amount, date=date_obj, category_id=category.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

def update_expense(db: Session, expense_id: int, title: str = None, amount: float = None, date_str: str = None, category_name: str = None):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return None
    
    if title:
        expense.title = title
    if amount:
        expense.amount = amount
    if date_str:
        expense.date = datetime.strptime(date_str, "%Y-%m-%d").date()
    if category_name:
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.commit()
            db.refresh(category)
        expense.category_id = category.id
        
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, expense_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        db.delete(expense)
        db.commit()
        return True
    return False

def get_all_expenses(db: Session):
    return db.query(Expense).all()
