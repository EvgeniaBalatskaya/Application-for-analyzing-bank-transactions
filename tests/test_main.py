import unittest

from unittest.mock import MagicMock, patch

from src.main import main


class TestMain(unittest.TestCase):
    @patch("src.main.read_excel")
    @patch("src.main.analyze_expenses")
    @patch("src.main.calculate_cashback")
    @patch("src.main.generate_report")
    def test_main(self, mock_generate_report, mock_calculate_cashback, mock_analyze_expenses, mock_read_excel):
        # Mock the return value of read_excel
        mock_read_excel.return_value = MagicMock(
            to_dict=MagicMock(return_value=[{"Категория": "Food", "Сумма операции": 100.0}])
        )

        # Mock the return values of analyze_expenses, calculate_cashback, generate_report
        mock_analyze_expenses.return_value = {"Food": 100.0}
        mock_calculate_cashback.return_value = {"Food": 5.0}
        mock_generate_report.return_value = '{"report": "data"}'  # Valid JSON

        # Patch the print function to check calls
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call('Categorized Expenses: {\n    "Food": 100.0\n}')
            mocked_print.assert_any_call('Cashback: {\n    "Food": 5.0\n}')
            mocked_print.assert_any_call('Generated Report: {\n    "report": "data"\n}')

    @patch("src.main.read_excel")
    def test_main_no_data(self, mock_read_excel):
        # Mock the return value of read_excel as None
        mock_read_excel.return_value = None

        # Patch the print function to check calls
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Не удалось загрузить данные из Excel-файла.")


if __name__ == "__main__":
    unittest.main()
