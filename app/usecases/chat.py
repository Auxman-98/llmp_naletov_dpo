from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.db.models import ChatMessage


async def ask(
    session: AsyncSession,
    system_instruction: str | None,
    prompt: str,
) -> str | None:
    """
    Запускает данный запрос пользователя на сервер с моделью через чат.
    В случае успеха возвращает ответ модели на запрос.

    Args:
    -----
        session (AsyncSession): асинхронная сессия, во время которой
    открыт и работает чат с моделью.
        system_instruction (str | None): опциональная системная
    инструкция, которую пользователь может задать перед началом общения.
        prompt (str): содержимое запроса пользователя.

    Returns:
    --------
        (str | None): результат обращения к серверу с запросом.
    В случае успеха - ответ модели в чате.
    """
    repo = ChatMessageRepository(session)
    messages = []

    if system_instruction:
        messages.append({
            "role" : "system",
            "content" : system_instruction,
        })
    for message in repo.chat_history:
        messages.append({
            "role" : message.role,
            "content" : message.content,
        })
    curr_message = await repo.create_chat_message(
        role=messages[-1]["role"],
        content=prompt,
    )
    messages.append({
        "role" : curr_message.role,
        "content" : curr_message.content,
    })

    client = OpenRouterClient()
    response = await client.generate(messages)
    if response:
        return response


async def show_history(
    session: AsyncSession,
    uid: int,
    max_history: int
) -> ChatMessage:
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
        (ChatMessage):
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
