import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_mask_card(three_letters_str: str, empty_str: str) -> None:
    assert get_mask_card_number(three_letters_str) == "Ошибка ввода, введите 16 цифровых значений"
    assert get_mask_card_number(empty_str) == "Ошибка ввода, введите 16 цифровых значений"


@pytest.mark.parametrize("input_data, expected", [("002436 000000000", "Ошибка ввода, введите 16 цифровых значений"),
                                                  ("asdfghjklzxcvbnm", "Ошибка ввода, введите 16 цифровых значений"),
                                                  ("1234567890123456", "1234 56** **** 3456")])


def test_mask_card_2(input_data: str, expected: str) -> None:
    assert get_mask_card_number(input_data) == expected


def test_mask_account(three_letters_str: str, empty_str: str) -> None:
    assert get_mask_account(three_letters_str) == "Ошибка ввода, введите 20 цифр"
    assert get_mask_account(empty_str) == "Ошибка ввода, введите 20 цифр"
    assert get_mask_account("1111002436 000000000") == "Ошибка ввода, введите 20 цифр"
    assert get_mask_account("asdfghjklzxcvbnmzpdn") == "Ошибка ввода, введите 20 цифр"
    assert get_mask_account("12345678901234567890") == "**7890"
