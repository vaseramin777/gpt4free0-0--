from __future__ import annotations  # Allows using class name in type hints

import json  # Used for encoding and decoding JSON data
from aiohttp import ClientSession  # Asynchronous HTTP client for Python

from ..typing import AsyncResult, Messages  # Importing custom types
from .base_provider import AsyncGeneratorProvider  # Importing base class
from .helper import get_random_string  # Importing helper function

class ChatgptDemoAi(AsyncGeneratorProvider):  # Class representing a ChatGPT demo AI provider
    url = "https://chat.chatgptdemo.ai"  # Base URL for the API
    working = False  # Flag indicating if the provider is currently working
    supports_gpt_35_turbo = True  # Flag indicating support for GPT-3.5-turbo model
    supports_message_history = True  # Flag indicating support for message history

    @classmethod
    async def create_async_generator(  # Class method creating an asynchronous generator
        cls,
        model: str,  # Model name
        messages: Messages,  # List of messages
        proxy: str = None,  # Optional proxy for HTTP requests
        **kwargs  # Additional keyword arguments
    ) -> AsyncResult:  # Asynchronous result object
        headers = {
            # HTTP headers for the request
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/",
            "Content-Type": "application/json",
            "Origin": cls.url,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        async with ClientSession(headers=headers) as session:  # Creating an asynchronous HTTP session
            data = {
                "botId": "default",
                "customId": "8824fe9bdb323a5d585a3223aaa0cb6e",
                "session": "N/A",
                "chatId": get_random_string(12),
                "contextId": 2,
                "messages": messages,
                "newMessage": messages[-1]["content"],
                "stream": True
            }
            async with session.post(f"{cls.url}/wp-json/mwai-ui/v1/chats/submit", json=data, proxy=proxy) as response:
                response.raise_for_status()  # Raise an exception if the response status is not 2xx
                async for chunk in response.content:
                    if chunk.startswith(b"data: "):
                        data = json.loads(chunk[6:])  # Decode JSON data from the response
