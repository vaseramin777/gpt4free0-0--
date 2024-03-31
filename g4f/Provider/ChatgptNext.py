from __future__ import annotations

import json
from aiohttp import ClientSession

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider
from .helper import format_prompt

class ChatgptNext(AsyncGeneratorProvider):
    """
    A class that provides an asynchronous generator for generating responses from the ChatGPT API.
    """
    url = "https://www.chatgpt-free.cc"
    working = True
    supports_gpt_35_turbo = True

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            **kwargs
    ) -> AsyncResult:
        """
        Create an asynchronous generator that yields chunks of data from the ChatGPT API.

        :param model: The model to use for the API request. Defaults to "gpt-3.5-turbo".
        :param messages: The messages to send to the API.
        :param proxy: An optional proxy to use for the API request.
        :param kwargs: Additional keyword arguments to pass to the API request.
        :return: An asynchronous generator that yields chunks of data from the API.
        """
    if not model:
        model = "gpt-3.5-turbo"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/event-stream",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Referer": "https://chat.fstha.com/",
        "x-requested-with": "XMLHttpRequest",
        "Origin": "https://chat.fstha.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Authorization": "Bearer ak-chatgpt-nice",
        "Connection": "keep-alive",
        "Alt-Used": "chat.fstha.com",
    }
    async with ClientSession(headers=headers) as session:
        """
        Create an asynchronous context manager for the aiohttp ClientSession.

        :param headers: The headers to use for the session.
        """
        data = {
            "messages": messages,
            "stream": True,
            "model": model,
            "temperature": 0.5,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "top_p": 1,
            **kwargs
        }
        async with session.post(f"https://chat.fstha.com/api/openai/v1/chat/completions", json=data, proxy=proxy) as response:
            """
            Send a POST request to the ChatGPT API.

            :param response: The response from the API.
            """
            response.raise_for_status()
            async for chunk in response.content:
                """
                Iterate over the chunks of data in the response.

                :param chunk: A chunk of data from the response.
                """
                if chunk.startswith(b"data: [DONE]"):
                    """

