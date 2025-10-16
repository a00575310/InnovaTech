import json, os, hashlib

def _data_path():
    return os.path.join(os.path.dirname(__file__), "users.json")

def _ensure_file():
    path = _data_path()
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f, ensure_ascii=False, indent=2)

def load_users():
    _ensure_file()
    with open(_data_path(), "r", encoding="utf-8") as f:
        return json.load(f).get("users", {})

def save_users(users: dict):
    with open(_data_path(), "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, ensure_ascii=False, indent=2)

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()
