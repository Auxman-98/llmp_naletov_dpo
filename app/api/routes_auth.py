from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import (
    register_user,
    login_user,
    get_user_by_id,
)
from app.api.deps import form_data, get_current_user
from app.db.session import get_session
from app.db.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    user = await register_user(
        session=session,
        email=data.email,
        password=data.password
    )
    reg_user = UserPublic(
        id=user.id,
        email=user.email,
        role="user",
    )

    return reg_user


@router.post("/login", response_model=TokenResponse)
async def login(
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    token = await login_user(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )

    return TokenResponse(access_token=token)


@router.get("/me")
async def get_authorized_user(
    session: AsyncSession = Depends(get_session),
) -> User:
    curr_user = await get_current_user(session=session)
    auth_user = await get_user_by_id(session, curr_user.id)

    return auth_user
