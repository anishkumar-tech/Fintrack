import sys
from database import init_db, get_db
from modules import expense_manager, budget_manager, subscription_manager, report_manager, search_manager

def print_menu():
    print("\n--- FinTrack Pro ---")
    print("1. Manage Expenses")
    print("2. Manage Subscriptions")
    print("3. Manage Budget")
    print("4. Generate Reports")
    print("5. Search Expenses")
    print("6. Exit")

def expense_menu(db):
    print("\n-- Expense Menu --")
    print("1. Add Expense")
    print("2. View All")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        title = input("Title: ")
        amount = float(input("Amount: "))
        date = input("Date (YYYY-MM-DD): ")
        category = input("Category: ")
        expense_manager.add_expense(db, title, amount, date, category)
        print("Expense added.")
    elif choice == '2':
        expenses = expense_manager.get_all_expenses(db)
        for e in expenses:
            print(f"{e.id} | {e.date} | {e.title} | {e.amount} | {e.category.name if e.category else 'No Category'}")
    elif choice == '3':
        eid = int(input("Expense ID: "))
        title = input("New Title (leave blank to keep): ")
        amount_str = input("New Amount (leave blank to keep): ")
        date = input("New Date (leave blank to keep): ")
        category = input("New Category (leave blank to keep): ")
        
        amount = float(amount_str) if amount_str else None
        
        expense_manager.update_expense(db, eid, title or None, amount, date or None, category or None)
        print("Expense updated.")
    elif choice == '4':
        eid = int(input("Expense ID: "))
        if expense_manager.delete_expense(db, eid):
            print("Expense deleted.")
        else:
            print("Expense not found.")

def subscription_menu(db):
    print("\n-- Subscription Menu --")
    print("1. Add Subscription")
    print("2. View Subscriptions")
    print("3. Delete Subscription")
    print("4. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        name = input("Name: ")
        amount = float(input("Amount: "))
        date = input("Next Due Date (YYYY-MM-DD): ")
        subscription_manager.add_subscription(db, name, amount, date)
        print("Subscription added.")
    elif choice == '2':
        subs = subscription_manager.get_subscriptions(db)
        for s in subs:
            print(f"{s.id} | {s.name} | {s.amount} | {s.next_date}")
    elif choice == '3':
        sid = int(input("Subscription ID: "))
        subscription_manager.delete_subscription(db, sid)
        print("Subscription deleted.")

def budget_menu(db):
    print("\n-- Budget Menu --")
    print("1. Set Budget")
    print("2. Check Budget")
    print("3. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        month = input("Month (YYYY-MM): ")
        limit = float(input("Limit: "))
        budget_manager.set_budget(db, month, limit)
        print("Budget set.")
    elif choice == '2':
        month = input("Month (YYYY-MM): ")
        res = budget_manager.check_budget(db, month)
        print(f"Budget Limit: {res['budget_limit']}")
        print(f"Total Spent: {res['total_spent']}")
        print(f"Remaining: {res['remaining']}")
        if res['exceeded']:
            print("ALERT: Budget Exceeded!")

def report_menu(db):
    print("\n-- Reports --")
    print("1. Category-wise Expenses")
    print("2. Monthly Expenses")
    print("3. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        results = report_manager.get_category_report(db)
        for row in results:
            print(f"Category: {row[0]}, Total: {row[1]}")
    elif choice == '2':
        results = report_manager.get_monthly_report(db)
        for row in results:
            print(f"Month: {row[0]}, Total: {row[1]}")

def search_menu(db):
    print("\n-- Search --")
    start = input("Start Date (YYYY-MM-DD): ")
    end = input("End Date (YYYY-MM-DD): ")
    results = search_manager.search_expenses_by_date(db, start, end)
    for row in results:
        print(f"{row.id} | {row.date} | {row.title} | {row.amount} | {row.name}")

def main():
    init_db()
    db_gen = get_db()
    db = next(db_gen)
    
    while True:
        print_menu()
        choice = input("Enter choice: ")
        
        try:
            if choice == '1':
                expense_menu(db)
            elif choice == '2':
                subscription_menu(db)
            elif choice == '3':
                budget_menu(db)
            elif choice == '4':
                report_menu(db)
            elif choice == '5':
                search_menu(db)
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Input Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
