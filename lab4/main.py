from fn_math_builtin import run_math_demo
from fn_datetime_builtin import run_datetime_demo
from fn_random_builtin import run_random_demo
from fn_os_builtin import run_os_demo
from fn_json_builtin import run_json_demo

from fn_requests_ext import run_requests_demo
from fn_colorama_ext import run_colorama_demo
from fn_rich_ext import run_rich_demo
from fn_faker_ext import run_faker_demo
from fn_qrcode_ext import run_qrcode_demo
from fn_tabulate_ext import run_tabulate_demo
from fn_emoji_ext import run_emoji_demo
from fn_pyfiglet_ext import run_pyfiglet_demo
from fn_humanize_ext import run_humanize_demo
from fn_tqdm_ext import run_tqdm_demo


def main() -> None:
    print("=== Запуск Лабораторної роботи №4 ===")
    run_math_demo()
    run_datetime_demo()
    run_random_demo()
    run_os_demo()
    run_json_demo()

    run_requests_demo()
    run_colorama_demo()
    run_rich_demo()
    run_faker_demo()
    run_qrcode_demo()
    run_tabulate_demo()
    run_emoji_demo()
    run_pyfiglet_demo()
    run_humanize_demo()
    run_tqdm_demo()
    print("\n=== Усі 15 модулів виконано ===")


if __name__ == "__main__":
    main()