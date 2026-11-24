from tabulate import tabulate


def run_tabulate_demo() -> None:
    rows = [["int", 4], ["str", 6], ["list", 8]]
    print("[tabulate] Таблиця даних:")
    print(tabulate(rows, headers=["Тип", "Значення"], tablefmt="github"))