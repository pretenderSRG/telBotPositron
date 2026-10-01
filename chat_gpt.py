import json
import logging

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AsyncOpenAI,
    RateLimitError,
)

from config import settings
from utils.utils import load_prompt

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.OPEN_API_KEY,
    timeout=settings.OPENAI_TIMEOUT,
)


async def complete(messages: list[dict[str, str]]) -> list[str] | str | None:
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            reasoning_effort=settings.OPENAI_REASONING,
            max_completion_tokens=settings.OPENAI_MAX_TOKENS,
        )
    except RateLimitError:
        logger.exception("Забагато спроб до OpenAI")
        return None
    except APITimeoutError:
        logger.exception("Сервер OpenAI не відповідає")
        return None
    except APIConnectionError:
        logger.exception("Не вийшло з'єднатися з OpenAI")
        return None
    except APIStatusError:
        logger.exception("Трапилась помилка відповіді від OpenAI")
        return None
    except Exception as exc:  # pragma: no cover - страховий запас
        logger.exception("Невідома помилка при запиті до OpenAI: %s", exc)
        return None

    content = response.choices[0].message.content or ""

    if not content:
        logger.warning("ChatGPT повернув порожню відповідь")
        return None

    if len(content) > 4096:
        result = []
        while content:
            part = content[:4096]
            content = content[4096:]
            result.append(part)
        return result

    return content


async def ask(
    system_prompt: str,
    user_message: str | None = None,
) -> list[str] | str | None:
    messages = [{"role": "system", "content": system_prompt}]

    if user_message:
        messages.append({"role": "user", "content": user_message})

    return await complete(messages)


async def ask_history(
    system_prompt: str,
    history: list[dict[str, str]] | str | None,
) -> list[str] | str | None:
    messages = [{"role": "system", "content": system_prompt}, *history]
    return await complete(messages)


async def check_person_exists(person: str) -> bool | None:
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": load_prompt("person_check"),
                },
                {"role": "user", "content": person},
            ],
            response_format={"type": "json_object"},
            reasoning_effort=settings.OPENAI_REASONING,
            max_completion_tokens=100,
        )
        content = response.choices[0].message.content
        result = json.loads(content or "")
        exists = result.get("exists")
        return exists if isinstance(exists, bool) else None
    except Exception:
        logger.exception("Не вдалося перевірити персонажа %s", person)
        return None
