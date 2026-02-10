from sqlalchemy.orm import Session
from models import Budget, Expense
from sqlalchemy import func
from datetime import datetime

def set_budget(db: Session, month: str, limit: float):
    # Month format YYYY-MM
    budget = db.query(Budget).filter(Budget.month == month).first()
    if budget:
        budget.limit = limit
    else:
        budget = Budget(month=month, limit=limit)
        db.add(budget)
    db.commit()
    return budget

def check_budget(db: Session, month: str):
    # Calculate total expenses for the month
    # Assuming month string is 'YYYY-MM'
    start_date = datetime.strptime(month + "-01", "%Y-%m-%d").date()
    # Simple logic to find end of month or just filter by string match if we stored date as string, 
    # but we stored date as Date object.
    
    # Extract year and month from the date column
    # SQLite STRFTIME('%Y-%m', date)
    
    total_spent = db.query(func.sum(Expense.amount)).filter(func.strftime("%Y-%m", Expense.date) == month).scalar() or 0.0
    
    budget = db.query(Budget).filter(Budget.month == month).first()
    limit = budget.limit if budget else 0.0
    
    return {
        "month": month,
        "total_spent": total_spent,
        "budget_limit": limit,
        "remaining": limit - total_spent,
        "exceeded": total_spent > limit if limit > 0 else False
    }
