from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import (
    register_user,
    login_user,
    get_user_by_id,
)
from app.api.deps import (
    security, form_data,
    get_session, get_current_user
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    user = await register_user(
        session=session,
        email=data.email,
        password=data.password,
    )
    reg_user = UserPublic(
        id=user.id,
        email=user.email,
        role="user",
    )

    return reg_user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: OAuth2PasswordRequestForm = form_data,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    token = await login_user(
        session=session,
        email=data.username,
        password=data.password,
    )

    return TokenResponse(access_token=token)


@router.get("/me")
async def get_authorized_user(
    token: Annotated[str, Depends(security)],
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    curr_user = await get_current_user(token, session)
    auth_user = await get_user_by_id(session, curr_user.id)
    user = UserPublic(
        id=auth_user.id,
        email=auth_user.email,
        role=auth_user.role,
    )

    return user
