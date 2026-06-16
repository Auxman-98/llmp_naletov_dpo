from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


async def ask(
    session: AsyncSession,
    system_instruction: str | None,
    prompt: str,
) -> str | None:
    repo = ChatMessageRepository(session)
    messages = []

    if system:
        messages.append({
            "role" : "system",
            "content" : system_instruction,
        })
    for message in repo.chat_history:
        messages.append({
            "role" : message.role,
            "content" : message.content,
        })
    messages.append({
        "role" : "user",
        "content" : prompt,
    })
    curr_message = await repo.create_chat_message(
        role=messages[-1]["role"],
        content=prompt,
    )

    client = OpenRouterClient()
    response = await client.generate(messages)
    if response:
        return response
