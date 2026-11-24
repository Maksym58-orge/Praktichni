import requests


def run_requests_demo() -> None:
    try:
        response = requests.get("https://httpbin.org/get", params={"lab": "4"}, timeout=5)
        print(f"[requests] Статус-код відповіді: {response.status_code}")
    except requests.RequestException as exc:
        print(f"[requests] Запит не виконано (немає мережі): {exc}")