from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import (
    ChatRequest, ChatResponse, ChatHistory
)
from app.usecases.chat import (
    ask,
    show_history,
    delete_history
)
from app.api.deps import (security,
    get_session, get_current_user
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def get_response(
    token: Annotated[str, Depends(security)],
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
) -> ChatResponse:
    curr_user = await get_current_user(token, session)
    answer = await ask(
        session,
        curr_user.id,
        request.prompt,
        request.system,
        request.temperature
    )

    return ChatResponse(answer=answer)


@router.get("/history", response_model=ChatHistory)
async def get_chat_history(
    token: Annotated[str, Depends(security)],
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
) -> ChatHistory:
    curr_user = await get_current_user(token, session)
    chat_history = await show_history(
        session,
        curr_user.id,
        request.max_history
    )

    return ChatHistory(items=chat_history)


@router.delete("/history")
async def delete_chat_history(
    token: Annotated[str, Depends(security)],
    session: AsyncSession = Depends(get_session)
) -> None:
    curr_user = await get_current_user(token, session)
    await delete_history(session, curr_user.id)
