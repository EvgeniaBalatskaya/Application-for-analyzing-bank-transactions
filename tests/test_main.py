import unittest

from unittest.mock import MagicMock, patch

from src.main import main


class TestMain(unittest.TestCase):
    @patch("src.main.read_excel")
    @patch("src.main.analyze_expenses")
    @patch("src.main.calculate_cashback")
    @patch("src.main.generate_report")
    def test_main(self, mock_generate_report, mock_calculate_cashback, mock_analyze_expenses, mock_read_excel):
        mock_read_excel.return_value = MagicMock(
            to_dict=MagicMock(return_value=[{"category": "Food", "amount": 100.0}])
        )

        mock_analyze_expenses.return_value = {"Food": 100.0}
        mock_calculate_cashback.return_value = {"Food": 5.0}
        mock_generate_report.return_value = "Report"

        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Categorized Expenses: {'Food': 100.0}")
            mocked_print.assert_any_call("Cashback: {'Food': 5.0}")
            mocked_print.assert_any_call("Generated Report: Report")

    @patch("src.main.read_excel")
    def test_main_no_data(self, mock_read_excel):
        mock_read_excel.return_value = None

        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Не удалось загрузить данные из Excel-файла.")


if __name__ == "__main__":
    unittest.main()
