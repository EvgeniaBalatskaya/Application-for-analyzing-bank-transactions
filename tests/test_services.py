import pytest
from src.services import calculate_category_total, get_category_average, process_report

# Мокируем данные для category_data
@pytest.fixture(autouse=True)
def mock_category_data():
    """
    Фикстура для мокирования данных в category_data перед каждым тестом.
    """
    from src.services import category_data
    category_data.clear()  # Очищаем предыдущие данные
    category_data.update({
        'Food': 100.0,
        'Transport': 50.0,
        'Entertainment': 200.0,
    })

# Тест для функции calculate_category_total
def test_calculate_category_total() -> None:
    """
    Тестирует функцию calculate_category_total для проверки корректности
    расчета общей суммы по категории.
    """
    # Проверка правильной суммы по категории 'Food'
    result = calculate_category_total('Food')
    assert result == 100.0, f"Expected 100.0 but got {result}"

    # Проверка, что для несуществующей категории возвращается 0.0
    result = calculate_category_total('Shopping')
    assert result == 0.0, f"Expected 0.0 but got {result}"


# Тест для функции get_category_average
def test_get_category_average() -> None:
    """
    Тестирует функцию get_category_average для проверки расчета среднего
    значения по всем категориям.
    """
    # Проверка, что возвращается правильное среднее
    result = get_category_average('Food')
    assert result == 116.66666666666667, f"Expected 116.6667 but got {result}"

    # Проверка, что при отсутствии категории возвращается 0.0
    result = get_category_average('Shopping')
    assert result == 0.0, f"Expected 0.0 but got {result}"


# Тест для функции process_report
def test_process_report() -> None:
    """
    Тестирует функцию process_report для проверки корректности обработки отчета.
    """
    # Задание данных
    data = {
        'Food': 100.0,
        'Transport': 50.0,
        'Entertainment': 200.0,
    }

    # Проверка, что возвращается правильное среднее
    result = process_report(data)
    assert result == 116.66666666666667, f"Expected 116.6667 but got {result}"

    # Проверка на пустые данные
    result = process_report({})
    assert result == 0.0, f"Expected 0.0 but got {result}"
