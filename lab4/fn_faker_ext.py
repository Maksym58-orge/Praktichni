from faker import Faker


def run_faker_demo() -> None:
    fake = Faker()
    print(f"[faker] Тестовий користувач: {fake.name()} ({fake.email()})")