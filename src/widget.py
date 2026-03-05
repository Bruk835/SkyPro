from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(incoming_data: str) -> str:
    """Функция, маскирующая номер счёта или карты"""

    if len(incoming_data) == 0:
        return "Ошибка, введите необходимую информацию"
    else:
        data_split = incoming_data.split()
        number = data_split[-1]
        name = " ".join(data_split[:-1])
        valid_names = ["visa platinum", "maestro", "visa classic", "visa gold", "mastercard", "счет"]

        if not number.isdigit():
            return "Неправильный формат данных"
        elif len(number) != 16 and len(number) != 20:
            return "Неправильно введён номер счета/карты"
        else:
            if name.lower() not in valid_names:
                return "Неправильный ввод названия карты/счета"
            else:
                if name.lower() == "счет":
                    masked_number = get_mask_account(number)
                else:
                    masked_number = get_mask_card_number(number)

                return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Функция преобразования формата даты "2024-03-11T02:26:18.671407" в формат "ДД.ММ.ГГГГ"."""

    if len(date_str) == 0:
        return "Ошибка, введите необходимую информацию"
    else:
        if not date_str[:4].isdigit():
            return "Ошибка ввода данных"
        else:
            if not date_str[5:7].isdigit():
                return "Ошибка ввода данных"
            else:
                if not date_str[8:10].isdigit():
                    return "Ошибка ввода данных"
                else:
                    year = date_str[0:4]
                    month = date_str[5:7]
                    day = date_str[8:10]

                return f"{day}.{month}.{year}"
