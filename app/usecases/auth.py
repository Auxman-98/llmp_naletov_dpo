from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (hash_password, verify_password,
    create_access_token)
from app.db.models import User
from app.repositories.users import UserRepository
from app.core.errors import (UserAlreadyExistsError, UnauthorizedError,
    NotFoundError)


async def register_user(
    session: AsyncSession,
    email: str,
    password: str
) -> User | None:
    repo = UserRepository(session)
    if repo.get_user_by_email(email):
        raise UserAlreadyExistsError(field="email")

    password_hash = hash_password(password)

    user = await repo.create_user(email, password_hash)

    return user


async def login_user(
    session: AsyncSession,
    email: str,
    password: str
) -> str:
    repo = UserRepository(session)
    user = await repo.get_user_by_email(email)

    if not user:
        raise UnauthorizedError()

    if not verify_password(password, user.password_hash):
        raise UnauthorizedError()

    token = create_access_token(sub=str(user.id))

    return token


async def get_user_by_id(
     session: AsyncSession,
     uid: int
) -> User:
     repo = UserRepository(session)
     user = await repo.get_user_by_id(uid)

     if not user:
         raise NotFoundError(f"Пользователь {uid}")

     return user
