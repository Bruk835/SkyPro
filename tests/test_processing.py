from src.processing import filter_by_state, sort_by_date


def test_filter_state(empty_list: list, three_letters_list: list) -> None:
    assert filter_by_state(empty_list) == "Ошибка ввода данных"
    assert filter_by_state(three_letters_list) == "Ошибка ввода данных"
    assert (
        filter_by_state([{"id": 41428829, "stat": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}])
        == "Ошибка ввода данных"
    )
    assert (
        filter_by_state([{"id": 41428829, "state": "EXECUTE", "date": "2019-07-03T18:35:29.512364"}])
        == "Ошибка ввода данных"
    )
    assert filter_by_state([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}]) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
    ]


def test_sort_date(empty_list: list, three_letters_list: list, empty_str: str, three_letters_str: str) -> None:
    assert sort_by_date(empty_list) == "Ошибка ввода данных"
    assert sort_by_date(three_letters_list) == "Ошибка ввода данных"
    assert (
        sort_by_date([{"id": 41428829, "state": "EXECUTED", "dat": "2019-07-03T18:35:29.512364"}])
        == "Ошибка ввода данных"
    )
    assert sort_by_date([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}]) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
    ]
