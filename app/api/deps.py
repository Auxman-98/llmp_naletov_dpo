from fastapi import Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.db.models import User
from app.usecases.auth import get_user_by_id


security = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
form_data: OAuth2PasswordRequestForm = Depends()


async def get_session() -> AsyncSession:
    try:
        db = await AsyncSessionLocal()
        yield db
    finally:
        await db.close()


async def get_current_user(
    token: str = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    """
    Возвращает данные о текущем пользователе сервиса в Swagger UI.

    Args:
        token (str) : уникальный токен данной пользовательской сессии.
        session (AsyncSession) : сессия во внутренней БД.

    Returns:
        User : объект для текущего пользователя.

    Raises:
        HTTPException : ошибка авторизации пользователя.
    """
    payload = decode_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="user unauthorized",
        )

    user = get_user_by_id(session, user_id)

    return user
