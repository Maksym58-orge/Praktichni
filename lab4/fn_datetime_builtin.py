from datetime import datetime


def run_datetime_demo() -> None:
    now = datetime.now()
    print(f"[datetime] Поточний час: {now.strftime('%Y-%m-%d %H:%M:%S')}")