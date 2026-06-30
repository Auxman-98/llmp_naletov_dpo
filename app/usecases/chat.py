from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


async def ask(
    session: AsyncSession,
    uid: int,
    prompt: str,
    system: str | None,
    temperature: float
) -> str | None:
    """
    Запускает данный запрос пользователя на сервер с моделью через чат.
    В случае успеха возвращает ответ модели на запрос.

    Args:
    -----
        session (AsyncSession):
    асинхронная сессия, во время которой открыт и работает чат с моделью.
        prompt (str):
    содержимое запроса пользователя.

    Returns:
    --------
        (str | None):
    результат обращения с запросом к серверу. В случае успеха - ответ модели в чате.
    """
    repo = ChatMessageRepository(session)
    messages = []

    for message in await repo.show_history(uid):
        messages.append({
            "role" : message["role"],
            "content" : message["content"]
        })
    curr_message = await repo.create_chat_message(
        uid=uid,
        role="user",
        content=prompt,
    )
    messages.append({
        "role" : curr_message.role,
        "content" : curr_message.content
    })

    client = OpenRouterClient()
    response = await client.generate(messages, system, temperature)
    if response:
        return response


async def show_history(
    session: AsyncSession,
    uid: int,
    max_history: int
) -> List[Dict]:
    """
    Показывает историю чата активного пользователя с моделью в соответствии
    с заданным максимальным количеством сохранённых сообщений.

    Args:
    -----
        session (AsyncSession):
    асинхронная сессия, во время которой запущен и работает чат с моделью.
        uid (int):
    ID активного пользователя для учёта сообщений.
        max_history (int):
    Заданное в настройках максимальное число сообщений, сохранённых в истории.

    Returns:
    --------
        (list[dict]):
    История чата с моделью в соответствии с пользовательскими настройками.
    """
    repo = ChatMessageRepository(session)
    chat_history = await repo.show_last_n_messages(
        uid=uid,
        n=max_history,
    )

    return chat_history


async def delete_history(
    session: AsyncSession,
    uid: int
) -> None:
    """
    Безвозвратно удаляет всю историю чата пользователя с моделью.

    Параметры:
    ----------
        session (AsyncSession):
    асинхронная сессия, во время которой запущен и работает чат с моделью.
        uid (int):
    ID активного пользователя для учёта сообщений.

    Возвращает:
    -----------
        (None):
    Функция не возвращает результат операции удаления.
    """
    repo = ChatMessageRepository(session)

    await repo.delete_chat_history(uid=uid)
