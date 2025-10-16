# app/profile_store.py
import os, json, datetime as _dt

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_DATA_PATH = os.path.join(_DATA_DIR, "profile.json")

def _ensure_dir():
    os.makedirs(_DATA_DIR, exist_ok=True)

def load():
    try:
        if os.path.exists(_DATA_PATH):
            with open(_DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f) or {}
    except Exception as e:
        print("profile_store.load error:", e)
    return {}

def _save(data: dict):
    _ensure_dir()
    try:
        with open(_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("profile_store._save error:", e)

def _stamp():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ----- Actualizaciones de secciones -----

def update_profile_basic(nombre=None, sector=None, tiempo=None):
    data = load()
    data.setdefault("profile", {})
    if nombre is not None: data["profile"]["nombre"] = nombre
    if sector is not None: data["profile"]["sector"] = sector
    if tiempo is not None: data["profile"]["tiempo"] = tiempo
    data["updated_at"] = _stamp()
    _save(data)

def update_form_answers(web, ecommerce, rrss, usa_software, software_nombre, alianzas):
    data = load()
    data.setdefault("form", {})
    data["form"].update({
        "web": web, "ecommerce": ecommerce, "rrss": rrss,
        "usa_software": usa_software, "software_nombre": software_nombre,
        "alianzas": alianzas
    })
    data["updated_at"] = _stamp()
    _save(data)

def update_action_plan(score, level, plan_text):
    data = load()
    data["action_plan"] = {
        "score": score,
        "level": level,
        "plan_text": plan_text,
        "updated_at": _stamp()
    }
    data["updated_at"] = _stamp()
    _save(data)
