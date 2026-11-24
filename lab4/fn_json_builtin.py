import json


def run_json_demo() -> None:
    payload = {"lab": 4, "files_count": 16, "status": "ok"}
    encoded = json.dumps(payload, ensure_ascii=False)
    print(f"[json] Серіалізований JSON: {encoded}")