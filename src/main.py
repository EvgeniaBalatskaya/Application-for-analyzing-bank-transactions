import json
import logging
from datetime import datetime
import pandas as pd
from src.views import main_page
from src.utils import load_user_settings, read_transactions

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_main():
    """
    Основная функция для запуска приложения.
    """
    date_str = "2025-03-31 12:52:05"  # Пример даты и времени
    transactions_file = "data/operations.xlsx"
    user_settings_file = "user_settings.json"

    transactions = read_transactions(transactions_file)
    user_settings = load_user_settings(user_settings_file)

    response = main_page(date_str, transactions, user_settings)

    print(json.dumps(response, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    run_main()