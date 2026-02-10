import unittest
from datetime import date
from database import init_db, get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules import expense_manager, budget_manager, subscription_manager, search_manager, report_manager

class TestFinTrack(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(self.engine)

    def test_add_expense(self):
        expense = expense_manager.add_expense(self.db, "Coffee", 5.0, "2023-10-01", "Food")
        self.assertEqual(expense.title, "Coffee")
        self.assertEqual(expense.amount, 5.0)
        self.assertEqual(expense.category.name, "Food")

    def test_update_expense(self):
        expense = expense_manager.add_expense(self.db, "Coffee", 5.0, "2023-10-01", "Food")
        updated = expense_manager.update_expense(self.db, expense.id, amount=6.0)
        self.assertEqual(updated.amount, 6.0)

    def test_delete_expense(self):
        expense = expense_manager.add_expense(self.db, "Coffee", 5.0, "2023-10-01", "Food")
        deleted = expense_manager.delete_expense(self.db, expense.id)
        self.assertTrue(deleted)
        self.assertIsNone(expense_manager.update_expense(self.db, expense.id, amount=10.0))

    def test_budget(self):
        budget_manager.set_budget(self.db, "2023-10", 100.0)
        expense_manager.add_expense(self.db, "Coffee", 50.0, "2023-10-01", "Food")
        res = budget_manager.check_budget(self.db, "2023-10")
        self.assertEqual(res['remaining'], 50.0)
        self.assertFalse(res['exceeded'])
        
        expense_manager.add_expense(self.db, "Dinner", 60.0, "2023-10-02", "Food")
        res = budget_manager.check_budget(self.db, "2023-10")
        self.assertTrue(res['exceeded'])

    def test_subscription(self):
        sub = subscription_manager.add_subscription(self.db, "Netflix", 15.0, "2023-11-01")
        self.assertEqual(sub.name, "Netflix")
        self.assertEqual(len(subscription_manager.get_subscriptions(self.db)), 1)
        subscription_manager.delete_subscription(self.db, sub.id)
        self.assertEqual(len(subscription_manager.get_subscriptions(self.db)), 0)

    def test_search(self):
        expense_manager.add_expense(self.db, "Coffee", 5.0, "2023-10-01", "Food")
        results = search_manager.search_expenses_by_date(self.db, "2023-10-01", "2023-10-01")
        self.assertEqual(len(results), 1)

    def test_report(self):
        expense_manager.add_expense(self.db, "Coffee", 5.0, "2023-10-01", "Food")
        expense_manager.add_expense(self.db, "Dinner", 15.0, "2023-10-01", "Food")
        results = report_manager.get_category_report(self.db)
        # Check result format (Category Name, Total Amount)
        self.assertEqual(results[0][0], "Food")
        self.assertEqual(results[0][1], 20.0)

if __name__ == "__main__":
    unittest.main()
