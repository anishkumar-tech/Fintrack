from database import init_db, get_db
from modules import expense_manager, budget_manager, subscription_manager

def seed():
    init_db()
    db = next(get_db())
    
    print("Seeding data...")
    
    # Expenses
    expense_manager.add_expense(db, "Groceries", 50.0, "2023-10-01", "Food")
    expense_manager.add_expense(db, "Internet", 60.0, "2023-10-05", "Utilities")
    expense_manager.add_expense(db, "Dinner", 30.0, "2023-10-08", "Food")
    expense_manager.add_expense(db, "Bus Fare", 2.5, "2023-10-10", "Transport")
    
    # Subscriptions
    subscription_manager.add_subscription(db, "Netflix", 15.0, "2023-11-01")
    
    # Budget
    budget_manager.set_budget(db, "2023-10", 100.0)
    
    print("Data seeded.")

if __name__ == "__main__":
    seed()
