import pandas as pd
import json
import os


def read_transactions(file_path: str) -> pd.DataFrame:
    """
    Читает транзакции из Excel-файла.

    :param file_path: Путь до файла.
    :return: DataFrame с транзакциями.
    :raises FileNotFoundError: Если файл не найден.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    return pd.read_excel(file_path)


def load_user_settings(file_path: str) -> dict:
    """
    Загружает пользовательские настройки из JSON-файла.

    :param file_path: Путь до файла.
    :return: Словарь с пользовательскими настройками.
    :raises FileNotFoundError: Если файл не найден.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    return settings
