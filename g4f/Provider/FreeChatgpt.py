from __future__ import annotations  # Allows using class name in type hints

import json  # Used to parse and serialize JSON data
import random  # Used to randomly select a URL from the list
from aiohttp import ClientSession  # Used to make asynchronous HTTP requests

from ..typing import AsyncResult, Messages  # Importing custom types
from .base_provider import AsyncGeneratorProvider  # Importing the base class

# A dictionary mapping model names to their corresponding internal names
models = {
    "claude-v2": "claude-2.0",
    "claude-v2.1": "claude-2.1",
    "gemini-pro": "google-gemini-pro"
}

# A list of URLs for the API endpoints
urls = [
    "https://free.chatgpt.org.uk",
    "https://ai.chatgpt.org.uk"
]

class FreeChatgpt(AsyncGeneratorProvider):
    # The base URL for API requests
    url = "https://free.chatgpt.org.uk"
    # A flag indicating whether the provider is working or not
    working = True
    # Flags indicating support for specific models
    supports_gpt_35_turbo = True
    supports_gpt_4 = True
    supports_message_history = True

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            **kwargs
    ) -> AsyncResult:
        """
        Create an asynchronous generator for the provider.

        :param model: The model to use for the request.
        :param messages: The messages to send to the model.
        :param proxy: The proxy to use for the request.
        :param kwargs: Additional keyword arguments.
        :return: An asynchronous generator.
        """
        # Map the provided model name to its internal name
        if model in models:
            model = models[model]
        # If no model is provided, use 'gpt-3.5-turbo' as the default
        elif not model:
            model = "gpt-3.5-turbo"

        # Select a random URL from the list
        url = random.choice(urls)

        # Prepare headers for the request
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Host": "free.chatgpt.org.uk",
            "Referer": f"{cls.url}/",
            "Origin": f"{cls.url}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        async with ClientSession(headers=headers) as session:
            # Prepare data for the request
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

            async with session.post(f'{url}/api/openai/v1/chat/completions', json=data, proxy=proxy) as response:
                # Check if the request was successful
                response.raise_for_status()

                started = False  # A flag indicating whether a response has been received

                # Iterate over the response content line by line
                async for line in response.content:
                    # Check if the line indicates the end of the response
                    if line.startswith(b"data: [DONE]"):
                        break
                    # Check if the line contains JSON data
                    elif line.startswith(b"data: "):
                
