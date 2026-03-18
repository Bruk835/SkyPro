from typing import Dict, List


def filter_by_state(dict_state: List[Dict], state: str = "EXECUTED") -> str | List[Dict]:
    """Функция сортировки операций по статусу, по умолчании статус операции EXECUTED"""

    filter_dict_state = []

    if len(dict_state) == 0:
        return "Ошибка ввода данных"
    else:
        if type(dict_state) is not list:
            return "Ошибка ввода данных"
        else:
            for operation in dict_state:
                if not isinstance(operation, dict):
                    return "Ошибка ввода данных"
                else:
                    if operation.get("state") == state:
                        filter_dict_state.append(operation)
                    else:
                        return "Ошибка ввода данных"

            return filter_dict_state


def sort_by_date(dict_date: List[Dict], sort_descending: bool = True) -> str | List[Dict]:
    """Функция сортировки данных по дате, по умолчанию сортировка в порядке убывания"""

    if len(dict_date) == 0:
        return "Ошибка ввода данных"
    else:
        if type(dict_date) is not list:
            return "Ошибка ввода данных"
        else:
            for operation in dict_date:
                if not isinstance(operation, dict) or "date" not in operation:
                    return "Ошибка ввода данных"
                else:
                    sorted_dict_by_date = sorted(dict_date, key=lambda x: x.get("date", ""), reverse=sort_descending)

            return sorted_dict_by_date
