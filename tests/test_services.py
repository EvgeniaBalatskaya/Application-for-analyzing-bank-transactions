import unittest

from src.services import analyze_expenses, calculate_cashback


class TestUtils(unittest.TestCase):
    def test_calculate_cashback(self):
        spending = {"Food": 200.0, "Transport": 50.0, "Entertainment": 100.0}
        expected_cashback = {"Food": 10.0, "Transport": 1.5, "Entertainment": 7.0}
        actual_cashback = calculate_cashback([], spending)

        self.assertAlmostEqual(actual_cashback["Food"], expected_cashback["Food"], places=2)
        self.assertAlmostEqual(actual_cashback["Transport"], expected_cashback["Transport"], places=2)
        self.assertAlmostEqual(actual_cashback["Entertainment"], expected_cashback["Entertainment"], places=2)

    def test_analyze_expenses(self):
        expenses = [
            {"category": "Food", "amount": 200.0},
            {"category": "Transport", "amount": 50.0},
            {"category": "Entertainment", "amount": 100.0},
            {"category": "Food", "amount": 50.0},
        ]
        expected_categorized_expenses = {"Food": 250.0, "Transport": 50.0, "Entertainment": 100.0}
        self.assertEqual(analyze_expenses(expenses), expected_categorized_expenses)


if __name__ == "__main__":
    unittest.main()
