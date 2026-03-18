from typing import Any, Union


def get_mask_card_number(card_number: Union[int, str], count_mask: int = 6) -> str:
    """Функция вывода номера карты, в котором часть числовых значений принимают символ "*" """

    # Преобразуем число в строку, если это необходимо
    card_number = str(card_number)

    if len(card_number) != 16:
        return "Ошибка ввода, введите 16 цифровых значений"
    else:
        if not card_number.isdigit():
            return "Ошибка ввода, введите 16 цифровых значений"
        else:
            masked = card_number[:6] + "*" * count_mask + card_number[-4:]
            # Разбиваем на блоки по 4 символа
            blocks = [masked[i:i + 4] for i in range(0, len(masked), 4)]
            # Объединяем блоки с пробелами
            result = " ".join(blocks)
        return result


def get_mask_account(account_number: Any, count_mask: int = 2) -> Any:
    """Функция вывода номера счёта, в котором часть числовых значений принимают символ "*" """

    # Преобразуем число в строку, если необходимо
    account_number = str(account_number)

    if len(account_number) != 20:
        return "Ошибка ввода, введите 20 цифр"
    else:
        if not account_number.isdigit():
            return "Ошибка ввода, введите 20 цифр"
        else:
            masked = "*" * count_mask + account_number[-4:]

        return masked
