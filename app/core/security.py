import time
from typing import Any, Dict

import base64
from passlib.context import CryptContext
import jwt

from app.core.config import settings
from app.core.errors import UnauthorizedError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = base64.b64encode(settings.jwt_secret.encode("utf-8"))
ALGORITHM = settings.jwt_alg

ACCESS_TTL_SECONDS = 60 * settings.access_token_expire_minutes


def hash_password(password: str) -> str:
    """
    Создаёт безопасный хэш заданного пароля для хранения в базе данных SQLite.

    Args:
        - password (str): строка с паролем.

    Returns:
        str: хэш для хранения в базе данных.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    """
    Проверяет, что введённый пароль соответствует сохранённому по хэшу.

    Args:
        - password (str): пароль, который пользователь ввёл при логине.
        - hashed_password (str): хэш пароля, который хранится в базе.

    Returns:
        bool: флаг (не-)соответствия введённого пароля сохранённому.
    """
    return pwd_context.verify(password, hashed_password)


def _now() -> int:
    return int(time.time())


def create_access_token(sub: str) -> str:
    payload = {
        "sub": sub,
        "type": "access",
        "iat": _now(),
        "exp": _now() + ACCESS_TTL_SECONDS,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError(message="Токен истёк")
    except jwt.InvalidTokenError:
        raise UnauthorizedError(message="Некорректный токен")

    if payload.get("type") != "access":
        raise UnauthorizedError(message="Неверный тип токена")
    
    return payload
