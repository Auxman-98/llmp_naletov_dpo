import httpx

from app.core.config import settings
from app.core.errors import (
    BadGatewayError, ServiceUnavailableError,
    GatewayTimeoutError
)


class OpenRouterClient():

    def __init__(
        self,
    ) -> None:
        self._api_key = settings.openrouter_api_key
        self.base_url = settings.openrouter_base_url
        self.model = settings.openrouter_model
        self.site_url = settings.openrouter_site_url
        self.app_name = settings.openrouter_app_name


    async def generate(
        self,
        messages: list[dict[str, str]],
        system: str | None,
        temperature: float
    ) -> str:
        url = f"{self.base_url}/chat/completions"
        async with httpx.AsyncClient(
            headers={
                "Authorization" : f"Bearer {self._api_key}",
                "HTTP-Referer" : str(self.site_url),
                "X-Title" : self.app_name,
                "Accept" : "application/json",
            },
            timeout=30.0,
        ) as client:
            payload_messages = []

            if system:
                payload_messages.append({
                    "role" : "system",
                    "content" : system
                })
            payload_messages.extend(messages)

            try:
                response = await client.post(
                    url=url,
                    json={
                        "model" : self.model,
                        "messages" : payload_messages,
                        "temperature" : temperature
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.TimeoutException:
                raise GatewayTimeoutError()
            except httpx.HTTPStatusError as exc:
                code = exc.response.status_code

                if code in (400, 401, 403, 404, 429, 502):
                    raise BadGatewayError()
                elif code == 503:
                    raise ServiceUnavailableError()
            except httpx.RequestError:
                raise ServiceUnavailableError()
