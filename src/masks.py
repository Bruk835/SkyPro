import logging
from typing import Any, Union

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/masks.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[int, str], count_mask: int = 6) -> str:
    """Функция вывода номера карты, в котором часть числовых значений принимают символ "*" """

    logger.debug(f"Вызов get_mask_card_number: {card_number}, count_mask={count_mask}")

    # Преобразуем число в строку, если это необходимо
    card_number = str(card_number)

    if len(card_number) != 16:
        error_msg = "Ошибка ввода, введите 16 цифровых значений"
        logger.error(f"{error_msg} (получено: {card_number})")
        return error_msg
    else:
        if not card_number.isdigit():
            error_msg = "Ошибка ввода, введите 16 цифровых значений"
            logger.error(f"{error_msg} (получено: {card_number})")
            return error_msg

        else:
            masked = card_number[:6] + "*" * count_mask + card_number[-4:]
            # Разбиваем на блоки по 4 символа
            blocks = [masked[i : i + 4] for i in range(0, len(masked), 4)]
            # Объединяем блоки с пробелами
            result = " ".join(blocks)
            logger.info(f"Карта замаскирована: {card_number} -> {result}")
        return result


def get_mask_account(account_number: Any, count_mask: int = 2) -> Any:
    """Функция вывода номера счёта, в котором часть числовых значений принимают символ "*" """

    logger.debug(f"Вызов get_mask_account: {account_number}, count_mask={count_mask}")

    # Преобразуем число в строку, если необходимо
    account_number = str(account_number)

    if len(account_number) != 20:
        error_msg = "Ошибка ввода, введите 20 цифровых значений"
        logger.error(f"{error_msg} (получено: {account_number})")
        return error_msg
    else:
        if not account_number.isdigit():
            error_msg = "Ошибка ввода, введите 20 цифр"
            logger.error(f"{error_msg} (получено: {account_number})")
            return error_msg
        else:
            masked = "*" * count_mask + account_number[-4:]
            logger.info(f"Счет замаскирован: {account_number} -> {masked}")
        return masked
