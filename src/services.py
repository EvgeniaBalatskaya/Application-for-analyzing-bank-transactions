import json
import re

from typing import Any, Dict, List


# Анализ выгодности категорий повышенного кешбэка
def cashback_analysis(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """
    Функция для анализа выгодности категорий для кешбэка.

    :param data: Список транзакций.
    :param year: Год, за который проводится анализ.
    :param month: Месяц, за который проводится анализ.
    :return: Словарь с категориями и суммами кешбэка.
    """
    category_totals: Dict[str, float] = {}
    for transaction in data:
        date = transaction["Дата операции"]
        if date.startswith(f"{year}-{month:02d}"):
            category = transaction["Категория"]
            cashback = transaction["Сумма операции"] * 0.05  # Пример кешбэка 5%
            category_totals[category] = category_totals.get(category, 0.0) + cashback

    return category_totals


# Инвесткопилка
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Функция для расчета суммы, которую можно отложить в Инвесткопилку.

    :param month: Месяц для расчета в формате 'YYYY-MM'.
    :param transactions: Список транзакций.
    :param limit: Предел округления в рублях.
    :return: Сумма, отложенная в Инвесткопилку.
    """
    total_investment: float = 0.0
    for transaction in transactions:
        date = transaction["Дата операции"]
        amount = transaction["Сумма операции"]

        # Проверяем, что транзакция происходит в указанном месяце
        if date.startswith(month):
            # Округляем сумму до ближайшего значения, кратного limit
            rounded_amount = (amount // limit + 1) * limit if amount % limit != 0 else amount
            total_investment += rounded_amount - amount

    return round(total_investment, 2)


# Простой поиск
def simple_search(data: List[Dict[str, Any]], query: str) -> str:
    """
    Функция для поиска всех транзакций, содержащих строку в описании или категории.
    """
    # Фильтрация транзакций, содержащих query в описании или категории
    filtered_data = filter(
        lambda transaction: query.lower() in transaction["Описание"].lower()
        or query.lower() in transaction["Категория"].lower(),
        data,
    )

    return json.dumps(list(filtered_data), ensure_ascii=False, indent=4)


# Поиск по телефонным номерам
def search_by_phone_number(data: List[Dict[str, Any]]) -> str:
    """
    Функция для поиска всех транзакций, содержащих мобильные номера в описании.
    """
    phone_number_pattern = r"\+?\d{1,2}[-\s]?\(?\d{1,4}\)?[-\s]?\d{1,4}[-\s]?\d{1,4}"

    # Фильтрация транзакций с мобильными номерами в описании
    filtered_data = filter(lambda transaction: re.search(phone_number_pattern, transaction.get("Описание", "")), data)

    return json.dumps(list(filtered_data), ensure_ascii=False, indent=4)


# Поиск переводов физическим лицам
def search_personal_transfers(data: List[Dict[str, Any]]) -> str:
    """
    Функция для поиска переводов физическим лицам по описанию.
    """
    transfer_pattern = r"[А-Яа-яЁё]+\s[А-Яа-яЁё]\."

    # Фильтрация переводов с именами в описании
    filtered_data = filter(
        lambda transaction: "Переводы" in transaction.get("Категория", "")
        and re.search(transfer_pattern, transaction.get("Описание", "")),
        data,
    )

    return json.dumps(list(filtered_data), ensure_ascii=False, indent=4)
