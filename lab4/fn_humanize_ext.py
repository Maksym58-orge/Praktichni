import humanize


def run_humanize_demo() -> None:
    print(f"[humanize] Розмір файлу: {humanize.naturalsize(15_728_640)}")