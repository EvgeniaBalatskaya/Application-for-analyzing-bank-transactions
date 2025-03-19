import json

from src.services import (
    cashback_analysis,
    investment_bank,
    search_by_phone_number,
    search_personal_transfers,
    simple_search,
)


# Тестовые данные
test_data = [
    {
        "Дата операции": "2025-03-01",
        "Категория": "Продукты",
        "Кешбэк": 100,
        "Описание": "Покупка продуктов в магазине",
    },
    {"Дата операции": "2025-03-02", "Категория": "Техника", "Кешбэк": 200, "Описание": "Покупка телевизора"},
    {"Дата операции": "2025-03-03", "Категория": "Продукты", "Кешбэк": 50, "Описание": "Покупка фруктов"},
    {"Дата операции": "2025-02-15", "Категория": "Кафе", "Кешбэк": 30, "Описание": "Ужин в кафе"},
    {"Дата операции": "2025-03-05", "Категория": "Техника", "Кешбэк": 150, "Описание": "Покупка компьютера"},
]


# Тесты для analyze_cashback_categories
def test_cashback_analysis() -> None:
    data = [
        {"Дата операции": "2025-03-01", "Сумма операции": 1000, "Описание": "Покупка", "Категория": "Продукты"},
        {"Дата операции": "2025-03-02", "Сумма операции": 2000, "Описание": "Покупка", "Категория": "Техника"},
        {"Дата операции": "2025-03-03", "Сумма операции": 500, "Описание": "Покупка", "Категория": "Продукты"},
        {"Дата операции": "2025-03-04", "Сумма операции": 1500, "Описание": "Покупка", "Категория": "Техника"},
    ]
    result = cashback_analysis(data, 2025, 3)
    expected = {
        "Продукты": 75.0,  # 1000 * 0.05 + 500 * 0.05
        "Техника": 175.0,  # 2000 * 0.05 + 1500 * 0.05
    }
    assert result == expected


# Тесты для investment_bank
def test_investment_bank() -> None:
    transactions = [
        {"Дата операции": "2025-03-01", "Сумма операции": 1712, "Описание": "Покупка", "Категория": "Продукты"},
        {"Дата операции": "2025-03-02", "Сумма операции": 2101, "Описание": "Покупка", "Категория": "Техника"},
        {"Дата операции": "2025-03-03", "Сумма операции": 1580, "Описание": "Покупка", "Категория": "Кафе"},
    ]
    result = investment_bank("2025-03", transactions, 50)
    assert result == 107.0  # Ожидаемый результат


# Тесты для simple_search
def test_simple_search() -> None:
    result = simple_search(test_data, "Техника")
    expected = [
        {"Дата операции": "2025-03-02", "Категория": "Техника", "Кешбэк": 200, "Описание": "Покупка телевизора"},
        {"Дата операции": "2025-03-05", "Категория": "Техника", "Кешбэк": 150, "Описание": "Покупка компьютера"},
    ]
    assert json.loads(result) == expected


# Тесты для search_by_phone_number
def test_search_by_phone_number() -> None:
    data_with_phone_numbers = [
        {"Дата операции": "2025-03-01", "Категория": "Продукты", "Кешбэк": 100, "Описание": "МТС +7 921 11-22-33"},
        {
            "Дата операции": "2025-03-02",
            "Категория": "Техника",
            "Кешбэк": 200,
            "Описание": "Тинькофф Мобайл +7 995 555-55-55",
        },
        {
            "Дата операции": "2025-03-03",
            "Категория": "Продукты",
            "Кешбэк": 50,
            "Описание": "МТС Mobile +7 981 333-44-55",
        },
        {"Дата операции": "2025-03-04", "Категория": "Кафе", "Кешбэк": 30, "Описание": "Ужин в кафе"},
    ]
    result = search_by_phone_number(data_with_phone_numbers)
    expected = [
        {"Дата операции": "2025-03-01", "Категория": "Продукты", "Кешбэк": 100, "Описание": "МТС +7 921 11-22-33"},
        {
            "Дата операции": "2025-03-02",
            "Категория": "Техника",
            "Кешбэк": 200,
            "Описание": "Тинькофф Мобайл +7 995 555-55-55",
        },
        {
            "Дата операции": "2025-03-03",
            "Категория": "Продукты",
            "Кешбэк": 50,
            "Описание": "МТС Mobile +7 981 333-44-55",
        },
    ]
    assert json.loads(result) == expected


# Тесты для search_personal_transfers
def test_search_personal_transfers() -> None:
    data_with_transfers = [
        {"Дата операции": "2025-03-01", "Категория": "Переводы", "Кешбэк": 100, "Описание": "Перевод Валерий А."},
        {"Дата операции": "2025-03-02", "Категория": "Переводы", "Кешбэк": 200, "Описание": "Перевод Сергей З."},
        {"Дата операции": "2025-03-03", "Категория": "Техника", "Кешбэк": 50, "Описание": "Покупка телефона"},
        {"Дата операции": "2025-03-04", "Категория": "Переводы", "Кешбэк": 150, "Описание": "Перевод Артем П."},
    ]
    result = search_personal_transfers(data_with_transfers)
    expected = [
        {"Дата операции": "2025-03-01", "Категория": "Переводы", "Кешбэк": 100, "Описание": "Перевод Валерий А."},
        {"Дата операции": "2025-03-02", "Категория": "Переводы", "Кешбэк": 200, "Описание": "Перевод Сергей З."},
        {"Дата операции": "2025-03-04", "Категория": "Переводы", "Кешбэк": 150, "Описание": "Перевод Артем П."},
    ]
    assert json.loads(result) == expected
