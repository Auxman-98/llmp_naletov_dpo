from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository():

    def __init__(self, session: AsyncSession) -> None:
        self._session = session


    async def show_history(
        self,
        uid: int,
    ) -> list[dict]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == uid)
            .order_by(
                ChatMessage.created_at.desc())
        )
        result = await self._session.execute(stmt)

        return result.mappings().all()

    async def create_chat_message(
        self,
        uid: int,
        role: str,
        content: str,
    ) -> ChatMessage:
        message = ChatMessage(
            user_id=uid,
            role="user",
            content=content,
        )
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)

        return message

    async def show_last_n_messages(
        self,
        uid: int,
        n: int
    ) -> list[dict]:
        stmt = (
            select(
                ChatMessage.id, ChatMessage.role,
                ChatMessage.content, ChatMessage.created_at)
            .where(ChatMessage.user_id == uid)
            .order_by(
                ChatMessage.created_at
            )
            .limit(n)
        )
        result = await self._session.execute(stmt)
        messages = result.mappings().all()

        return messages

    async def delete_chat_history(self, uid: int) -> None:
        stmt = (
            delete(ChatMessage)
            .where(ChatMessage.user_id == uid)
        )
        await self._session.execute(stmt)
        await self._session.commit()
