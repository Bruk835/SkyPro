from masks import get_mask_account, get_mask_card_number


def mask_account_card(incoming_data: str) -> str:
    """Функция, маскирующая номер счёта или карты"""

    data_split = incoming_data.split()
    number = data_split[-1]
    name = " ".join(data_split[:-1])

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Функция преобразования формата даты "2024-03-11T02:26:18.671407" в формат "ДД.ММ.ГГГГ"."""
    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]

    return f"{day}.{month}.{year}"
