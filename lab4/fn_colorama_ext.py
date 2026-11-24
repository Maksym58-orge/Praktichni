from colorama import Fore, Style, init


def run_colorama_demo() -> None:
    init(autoreset=True)
    print(f"{Fore.GREEN}[colorama] Кольоровий текст працює коректно.{Style.RESET_ALL}")