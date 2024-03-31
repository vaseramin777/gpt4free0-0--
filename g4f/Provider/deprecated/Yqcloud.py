from __future__ import annotations

import random
from ...requests import StreamSession

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, format_prompt


class Yqcloud(AsyncGeneratorProvider):
    """
    Yqcloud class is an asynchronous generator provider that communicates with the Yqcloud API to generate responses.
    It inherits from the AsyncGeneratorProvider class and implements the create_async_generator method.
    """

    url = "https://chat9.yqcloud.top/"
    working = True
    supports_gpt_35_turbo = True

    @staticmethod
    async def create_async_generator(
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        **kwargs,
    ) -> AsyncResult:
        """
        create_async_generator is a static method that creates an asynchronous generator to generate responses from the Yqcloud API.
        It takes in the model name, messages, proxy, timeout, and any number of keyword arguments.
        It creates a StreamSession object and sends a POST request to the Yqcloud API with the required payload.
        It then decodes the response and yields each chunk of data.
        If the IP address is blocked by abuse detection, it raises a RuntimeError.
        """
        async with StreamSession(
            headers=_create_header(), proxies={"https": proxy}, timeout=timeout
        ) as session:
            payload = _create_payload(messages, **kwargs)
            async with session.post("https://api.aichatos.cloud/api/generateStream", json=payload) as response:
                response.raise_for_status()
                async for chunk in response.iter_content():
                    if chunk:
                        chunk = chunk.decode()
                        if "sorry, 您的ip已由于触发防滥用检测而被封禁" in chunk:
                            raise RuntimeError("IP address is blocked by abuse detection.")
                        yield chunk


def _create_header():
    return {
        "accept"        : "application/json, text/plain, */*",
        "content-type"  : "application/json",
        "origin"        : "https://chat9.yqcloud.top",
        "referer"       : "https://chat9.yqcloud.top/"
    }


def _create_payload(
    messages: Messages,
    system_message: str = "",
    user_id: int = None,
    **kwargs
):
    """
    _create_payload is a function that creates the payload for the Yqcloud API request.
    It takes in the messages, system_message, user_id, and any number of keyword arguments.
    If no user_id is provided, it generates a random user_id.
    It then creates a payload with the required fields and returns it.
    """
    if not user_id:
        user_id = random.randint(1690000544336, 2093025
