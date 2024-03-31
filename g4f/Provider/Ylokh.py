from __future__ import annotations  # Allows using class name in type hints

import json

from ..requests import StreamSession  # Type hinting for StreamSession class
from .base_provider import AsyncGeneratorProvider  # Type hinting for AsyncGeneratorProvider class
from ..typing import AsyncResult, Messages  # Type hinting for AsyncResult and Messages types

class Ylokh(AsyncGeneratorProvider):
    # Class for Ylokh API provider
    url = "https://chat.ylokh.xyz"
    working = False
    supports_message_history = True 
    supports_gpt_35_turbo = True

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            stream: bool = True,
            proxy: str = None,
            timeout: int = 120,
            **kwargs
    ) -> AsyncResult:
        # Factory method to create an async generator for Ylokh API
        model = model if model else "gpt-3.5-turbo"
        headers = {"Origin": cls.url, "Referer": f"{cls.url}/"}
        data = {
            "messages": messages,
            "model": model,
            "temperature": 1,
            "presence_penalty": 0,
            "top_p": 1,
            "frequency_penalty": 0,
            "allow_fallback": True,
            "stream": stream,
            **kwargs
        }
        async with StreamSession(
                headers=headers,
                proxies={"https": proxy},
                timeout=timeout
            ) as session:
            # Create a StreamSession instance and set headers, proxies, and timeout
            async with session.post("https://chatapi.ylokh.xyz/v1/chat/completions", json=data) as response:
                # Send a POST request to the Ylokh API with data
                response.raise_for_status()  # Raise an exception if the response status code is not 2xx
                if stream:
                    async for line in response.iter_lines():
                        # If streaming is enabled, iterate over the lines of the response
                        line = line.decode()  # Decode the line from bytes to string
                        if line.startswith("data: "):
                            if line.startswith("data: [DONE]"):
                                # If the line indicates the end of the stream, break the loop
                                break
                            line = json.loads(line[6:])  # Parse the JSON data
                            content = line["choices"][0]["delta"].get("content")
                            if content:
                                yield content  # Yield the content if it exists
                else:
                    chat = await response.json()  # Parse the JSON data if streaming is disabled
                    yield chat["choices"][0]["message"].get("content")  # Yield the content
