from __future__ import annotations  # Allows using class name in type hints

import json
from aiohttp import ClientSession  # Asynchronous HTTP client

from ..typing import AsyncResult, Messages  # Custom types
from .base_provider import AsyncGeneratorProvider  # Base class for asynchronous generator providers
from .helper import get_random_string  # Helper function to generate random strings

class NoowAi(AsyncGeneratorProvider):
    # Class representing NoowAi provider
    url = "https://noowai.com"  # Base URL for NoowAi API
    supports_message_history = True  # Whether this provider supports message history
    supports_gpt_35_turbo = True  # Whether this provider supports GPT-3.5-turbo model
    working = False  # Whether this provider is currently working

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            **kwargs
    ) -> AsyncResult:
        # Class method to create an asynchronous generator
        headers = {
            # Request headers
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/",
            "Content-Type": "application/json",
            "Origin": cls.url,
            "Alt-Used": "noowai.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }
        async with ClientSession(headers=headers) as session:
            # Create an asynchronous context manager for aiohttp.ClientSession
            data = {
                # Request data
                "botId": "default",
                "customId": "d49bc3670c3d858458576d75c8ea0f5d",
                "session": "N/A",
                "chatId": get_random_string(),
                "contextId": 25,
                "messages": messages,
                "newMessage": messages[-1]["content"],
                "stream": True
            }
            async with session.post(f"{cls.url}/wp-json/mwai-ui/v1/chats/submit", json=data, proxy=proxy) as response:
                # Send a POST request to NoowAi API
                response.raise_for_status()  # Raise an exception if the response status code is not 2xx
                async for line in response.content:
                    # Iterate over response content line by line
                    if line.startswith(b"data: "):
                        # Check if the line starts with "data: "
                        try:
                            line = json.loads(line[6:])  # Decode the line as JSON
                            assert "type" in line  # Check if the JSON object has a "type" field
                        except:
                            raise RuntimeError(f"Broken line: {line.decode()}")  # Raise an exception if JSON decoding fails
                        if line["type"] == "live":
                            # If the type is "live", yield the data field
                            yield line["data"]
                        elif line["type"] == "end":
                            # If the type is "end", break the loop
                            break
                        elif line["type"] == "error":
                            # If
