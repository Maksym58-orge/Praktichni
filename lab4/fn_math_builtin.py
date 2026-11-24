import math


def run_math_demo() -> None:
    radius = 5
    area = math.pi * math.pow(radius, 2)
    print(f"[math] Площа кола з радіусом {radius}: {area:.2f}, ceil={math.ceil(area)}")