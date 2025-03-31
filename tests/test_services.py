import unittest

from src.services import analyze_expenses, calculate_cashback


class TestServices(unittest.TestCase):
    def test_calculate_cashback(self):
        spending = {"Food": 200.0, "Transport": 50.0, "Entertainment": 100.0}
        expected_cashback = {"Food": 10.0, "Transport": 1.5, "Entertainment": 7.0}
        cashback = calculate_cashback([], spending)
        self.assertEqual(cashback, expected_cashback)

    def test_analyze_expenses(self):
        expenses = [
            {"category": "Food", "amount": 200.0},
            {"category": "Transport", "amount": 50.0},
            {"category": "Entertainment", "amount": 100.0},
            {"category": "Food", "amount": 50.0},
        ]
        expected_analysis = {"Food": 250.0, "Transport": 50.0, "Entertainment": 100.0}
        analysis = analyze_expenses(expenses)
        self.assertEqual(analysis, expected_analysis)


if __name__ == "__main__":
    unittest.main()
