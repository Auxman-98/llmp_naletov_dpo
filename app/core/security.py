import time
from typing import Any, Dict

from passlib.context import CryptContext
import jwt

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.jwt_secret
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
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
