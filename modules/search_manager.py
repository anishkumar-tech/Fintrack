from sqlalchemy.orm import Session
from sqlalchemy import text

def search_expenses_by_date(db: Session, start_date: str, end_date: str):
    sql = text("""
        SELECT e.id, e.title, e.amount, e.date, c.name
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.date BETWEEN :start_date AND :end_date
    """)
    result = db.execute(sql, {"start_date": start_date, "end_date": end_date}).fetchall()
    return result
