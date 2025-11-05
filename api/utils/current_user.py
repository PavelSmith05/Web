from __future__ import annotations

from typing import Optional, Any


def resolve_request_user(request) -> Optional[Any]:
    """
    Унифицированное получение текущего пользователя с учётом анонимных сессий.
    Возвращает None, если пользователь не авторизован.
    """
    user = getattr(request, "user", None)
    if user is not None and getattr(user, "is_authenticated", False):
        return user
    return None

