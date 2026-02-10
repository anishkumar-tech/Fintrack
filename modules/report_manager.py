from sqlalchemy.orm import Session
from sqlalchemy import text

def get_category_report(db: Session):
    # Raw SQL query as requested
    sql = text("""
        SELECT c.name, SUM(e.amount) as total
        FROM categories c
        JOIN expenses e ON c.id = e.category_id
        GROUP BY c.name
    """)
    result = db.execute(sql).fetchall()
    return result

def get_monthly_report(db: Session):
    # Group by month
    sql = text("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """)
    result = db.execute(sql).fetchall()
    return result
