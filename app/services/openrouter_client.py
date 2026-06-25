import httpx

from app.core.config import settings
from app.core.errors import (
    BadGatewayError, ServiceUnavailableError,
    GatewayTimeoutError)


class OpenRouterClient():

    def __init__(
        self,
    ) -> None:
        self._api_key = settings.api_key
        self.base_url = settings.base_url
        self.model = settings.model
        self.site_url = settings.site_url
        self.app_name = settings.app_name


    async def generate(
        self,
        messages: list[dict[str, str]]
    ) -> str | None:
        url = f"{self.base_url}/chat/completions"
        async with httpx.AsyncClient(
            params={
                "model": self.model,
                "messages": messages,
            },
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "HTTP-Referer": self.site_url,
                "X-Title": self.app_name,
            },
        ) as client:

            try:
                response = await client.post(url)
                return response.json()["messages"][0]["content"]
            except httpx.TimeoutException:
                raise GatewayTimeoutError()
            except httpx.HTTPStatusError as exc:
                code = exc.response.status_code

                if code == 502 | 400 <= code < 500:
                    raise BadGatewayError()
                elif code == 503:
                    raise ServiceUnavailableError()
