# app/session.py
_current_user_email: str | None = None

def set_user(email: str | None) -> None:
    global _current_user_email
    _current_user_email = email

def get_user() -> str | None:
    return _current_user_email
