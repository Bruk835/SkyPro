from typing import List, Dict, Iterator


def filter_by_currency(dict_base: List[Dict], currency: str) -> Iterator[Dict]:
    """Функция фильтрации операций по типу валюты"""

    if not dict_base:
        raise ValueError("Ошибка ввода данных")
    for transaction in dict_base:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(dict_base: List[Dict]) -> Iterator[str]:
    """Генератор описания операций"""

    if not dict_base:
        raise ValueError("Ошибка ввода данных")
    for i, operation in enumerate(dict_base):
        description = operation.get("description")
        if description is None:
            print(f"Предупреждение: в транзакции {i} нет описания")
            continue
        yield description


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор номеров банковских карт"""

    if start < 1 or end > 9999999999999999:
        raise ValueError("Номер карты должен быть от 0000000000000001 до 9999999999999999")

    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    for number in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями слева до 16 цифр
        card_number = str(number).zfill(16)
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"

        yield formatted_number
