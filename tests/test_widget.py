from src.widget import mask_account_card, get_date


def test_mask_widget(empty_str: str, three_letters_str: str) -> None:
    assert mask_account_card(empty_str) == "Ошибка, введите необходимую информацию"
    assert mask_account_card(three_letters_str) == "Неправильный формат данных"
    assert mask_account_card("Visa Platinum") == "Неправильный формат данных"
    assert mask_account_card("Visa Platinum 1234567") == "Неправильно введён номер счета/карты"
    assert mask_account_card("Maestro 1234567") == "Неправильно введён номер счета/карты"
    assert mask_account_card("Visa Classic 1234567") == "Неправильно введён номер счета/карты"
    assert mask_account_card("Visa Gold 1234567") == "Неправильно введён номер счета/карты"
    assert mask_account_card("Visa Platinu 1111111111111111") == "Неправильный ввод названия карты/счета"
    assert mask_account_card("Счет 1234567") == "Неправильно введён номер счета/карты"
    assert mask_account_card("Visa Platinum 1111111111111111") == "Visa Platinum 1111 11** **** 1111"
    assert mask_account_card("Счет 11111111111111111111") == "Счет **1111"


def test_get_date(empty_str: str, three_letters_str: str) -> None:
    assert get_date(empty_str) == "Ошибка, введите необходимую информацию"
    assert get_date(three_letters_str) == "Ошибка ввода данных"
    assert get_date("20240-03-11T02:26:18.671407") == "Ошибка ввода данных"
    assert get_date("2024-030-11T02:26:18.671407") == "Ошибка ввода данных"
    assert get_date("-2024-03-11T02:26:18.671407") == "Ошибка ввода данных"
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
