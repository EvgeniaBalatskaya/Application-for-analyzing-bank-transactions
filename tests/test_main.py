import pytest
from unittest import mock
from services import process_transaction, convert_xlsx_to_json, write_transactions_to_json
from views import generate_report
from reports import generate_report_with_logging
import json


# Мок для API запросов
@pytest.fixture
def mock_api_responses():
    with mock.patch('requests.get') as mock_get:
        # Мокируем ответ для курсов валют
        mock_get.return_value.json.return_value = {
            "rates": {
                "EUR": 0.85
            }
        }
        yield mock_get


# Тест на обработку транзакции
def test_process_transaction(mock_api_responses):
    transaction = {
        "amount": 100,
        "category": "Food",
        "account_number": "1234567812345678"
    }

    # Вызываем обработку транзакции (конвертируем валюту)
    result = process_transaction(transaction, 'USD', 'EUR')

    # Проверяем, что сумма конвертирована
    assert result['amount_in_to_currency'] == '85.00'
    assert 'exchange_rate' in result
    assert result['exchange_rate'] == '0.85'


# Тест на конвертацию данных из XLSX в JSON
def test_convert_xlsx_to_json():
    # Мокируем pandas read_excel
    mock_transactions = [
        {"amount": 100, "category": "Food", "account_number": "1234567812345678"},
        {"amount": 50, "category": "Transport", "account_number": "8765432187654321"}
    ]
    with mock.patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value.to_dict.return_value = mock_transactions

        result = convert_xlsx_to_json('mock_file.xlsx')

        # Проверяем, что данные корректно конвертированы в формат JSON
        assert len(result) == 2
        assert result[0]["amount"] == 100


# Тест на запись транзакций в JSON
def test_write_transactions_to_json():
    transactions = [
        {"amount": 100, "category": "Food", "amount_in_to_currency": "85.00", "exchange_rate": "0.85"}
    ]
    with mock.patch('builtins.open', mock.mock_open()) as mock_open:
        write_transactions_to_json(transactions, 'mock_output.json')

        # Проверяем, что файл открылся и данные записались
        mock_open.assert_called_once_with('mock_output.json', 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with(json.dumps(transactions, ensure_ascii=False, indent=4))


# Тест на генерацию отчета
def test_generate_report():
    expenses = [{"category": "Food", "amount": 100}, {"category": "Transport", "amount": 50}]

    # Мокируем внешний API
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "rates": {
                "EUR": 0.85
            }
        }
        # Генерируем отчет
        result = generate_report(expenses)

        # Проверяем, что отчет содержит расходы, курсы валют и прочее
        report = json.loads(result)
        assert report["expenses"] == expenses
        assert "exchange_rates" in report
        assert "date" in report


# Тест на генерацию отчета с логированием
def test_generate_report_with_logging(mock_api_responses):
    expenses = [{"category": "Food", "amount": 100}, {"category": "Transport", "amount": 50}]

    # Мокируем работу с логами
    with mock.patch('logging.info') as mock_info:
        report = generate_report_with_logging(expenses)

        # Проверяем, что отчет был сгенерирован и логирование было выполнено
        assert isinstance(report, dict)
        mock_info.assert_called()
        assert "Generated Report" in str(mock_info.call_args[0])

