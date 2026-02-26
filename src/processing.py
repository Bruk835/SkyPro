from typing import Dict
from typing import List

def filter_by_state (dict_base: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """Функция сортировки операций по статусу, по умолчании статус операции EXECUTED"""

    filter_dicts = []
    for type in dict_base:
        if type.get('state') == state:
            filter_dicts.append(type)

    return filter_dicts


def sort_by_date(dict_base: List[Dict], sort_descending: bool = True) -> List[Dict]:
    """Функция сортировки данных по дате, по умолчанию сортировка в порядке убывания"""

    sorted_dict = sorted(dict_base, key=lambda x: x["date"], reverse=sort_descending)

    return sorted_dict
