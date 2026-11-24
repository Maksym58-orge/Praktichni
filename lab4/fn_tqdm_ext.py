import time
from tqdm import tqdm


def run_tqdm_demo() -> None:
    print("[tqdm] Прогрес-бар:")
    for _ in tqdm(range(10), desc="Обробка", leave=False):
        time.sleep(0.02)