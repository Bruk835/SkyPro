from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_curr_empty_list() -> None:
    """Тест обработки пустого списка"""
    with pytest.raises(ValueError, match="Ошибка ввода данных"):
        list(filter_by_currency([], "USD"))


@pytest.mark.parametrize(
    "currency, expected_count, expected_ids",
    [
        ("USD", 3, [939719570, 142264268, 895315941]),
        ("RUB", 2, [873106923, 594226727]),
        ("EUR", 0, []),
    ],
)
def test_filter_curr_mult_curr(
        transactions: List[Dict], currency: str, expected_count: int, expected_ids: str) -> None:
    """Параметризованный тест для разных валют"""
    generator = filter_by_currency(transactions, currency)
    result = list(generator)

    assert len(result) == expected_count
    assert [t["id"] for t in result] == expected_ids


def test_filter_curr_usd(transactions: List[Dict]) -> None:
    """Тест фильтрации USD транзакций"""
    generator = filter_by_currency(transactions, "USD")
    result = list(generator)

    assert len(result) == 3
    assert all(i["operationAmount"]["currency"]["code"] == "USD" for i in result)
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268
    assert result[2]["id"] == 895315941


def test_filter_curr_rub(transactions: List[Dict]) -> None:
    """Тест фильтрации RUB транзакций"""
    generator = filter_by_currency(transactions, "RUB")
    result = list(generator)

    assert len(result) == 2
    assert all(i["operationAmount"]["currency"]["code"] == "RUB" for i in result)
    assert result[0]["id"] == 873106923
    assert result[1]["id"] == 594226727


def test_filter_curr_nonex_curr(transactions: List[Dict]) -> None:
    """Тест фильтрации по несуществующей валюте"""
    generator = filter_by_currency(transactions, "EUR")
    result = list(generator)

    assert len(result) == 0


def test_filter_curr_next_func(transactions: List[Dict]) -> None:
    """Тест работы с next()"""
    generator = filter_by_currency(transactions, "USD")

    first = next(generator)
    assert first["id"] == 939719570

    second = next(generator)
    assert second["id"] == 142264268

    third = next(generator)
    assert third["id"] == 895315941

    with pytest.raises(StopIteration):
        next(generator)


def test_filter_curr_next_stop_iter(transactions: List[Dict]) -> None:
    """Тест исключения StopIteration"""
    generator = filter_by_currency(transactions, "EUR")

    with pytest.raises(StopIteration):
        next(generator)


def test_trans_descr_empty_list(empty_list: List[Dict]) -> None:
    """Тест обработки пустого списка"""
    with pytest.raises(ValueError, match="Ошибка ввода данных"):
        list(transaction_descriptions(empty_list))


def test_trans_descr_next_func(transactions: List[Dict]) -> None:
    """Тест работы с next()"""
    generator = transaction_descriptions(transactions)

    first = next(generator)
    assert first == "Перевод организации"

    second = next(generator)
    assert second == "Перевод со счета на счет"

    third = next(generator)
    assert third == "Перевод со счета на счет"

    forth = next(generator)
    assert forth == "Перевод с карты на карту"

    fifth = next(generator)
    assert fifth == "Перевод организации"

    with pytest.raises(StopIteration):
        next(generator)


def test_card_num_gen_basic() -> None:
    result = list(card_number_generator(20000099, 20000100))
    expected = ["0000 0000 2000 0099", "0000 0000 2000 0100"]
    assert result == expected


def test_card_num_gen_format() -> None:
    """Тест формата номера карты"""
    result = list(card_number_generator(1234567890123456, 1234567890123456))
    card_number = result[0]
    assert len(card_number) == 19  # 16 цифр + 3 пробела


def test_card_num_gen_end_too_large() -> None:
    with pytest.raises(ValueError, match="Номер карты должен быть от 0000000000000001 до 9999999999999999"):
        list(card_number_generator(1, 10000000000000000))


@pytest.mark.parametrize(
    "start,end,expected_count",
    [
        (3, 3, 1),
        (25004321, 25004327, 7),
        (9876543210, 9876543219, 10),
        (3333333333333333, 3333333333333336, 4),
    ],
)
def test_card_num_gen_parametrized(start: int, end: int, expected_count: int) -> None:
    """Параметризованный тест для разных диапазонов"""
    result = list(card_number_generator(start, end))
    assert len(result) == expected_count


def test_card_num_gen_edge_cases() -> None:
    """Тест граничных значений"""
    result_min = list(card_number_generator(1, 1))
    assert result_min[0] == "0000 0000 0000 0001"

    result_max = list(card_number_generator(9999999999999999, 9999999999999999))
    assert result_max[0] == "9999 9999 9999 9999"


def test_card_num_gen_is_iter() -> None:
    """Тест что функция действительно возвращает итератор"""
    generator = card_number_generator(3333, 3334)

    assert next(generator) == "0000 0000 0000 3333"
    assert next(generator) == "0000 0000 0000 3334"

    with pytest.raises(StopIteration):
        next(generator)
