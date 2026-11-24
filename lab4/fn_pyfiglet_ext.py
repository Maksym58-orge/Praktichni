import pyfiglet


def run_pyfiglet_demo() -> None:
    banner = pyfiglet.figlet_format("LAB 4", font="slant").strip()
    print(f"[pyfiglet]\n{banner}")