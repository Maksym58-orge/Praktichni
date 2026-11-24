import random


def run_random_demo() -> None:
    items = ["Python", "Git", "PyCharm", "Linux"]
    print(f"[random] Випадковий вибір: {random.choice(items)}, число={random.randint(1, 100)}")