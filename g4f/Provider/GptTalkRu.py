from __future__ import annotations  # Allows using class name in type hints

import aiohttp  # Asynchronous HTTP client/server for Python
from typing import AsyncResult, Messages  # Importing custom types

from .base_provider import AsyncGeneratorProvider  # Base asynchronous generator provider


class GptTalkRu(AsyncGeneratorProvider):
    """
    GptTalkRu class is an asynchronous generator provider for interacting with the GptTalkRu API.
    """

    url = "https://gpttalk.ru"
    working = True
    supports_gpt_35_turbo = True

    @classmethod
    async def create_async_generator(
        cls,  # Class method, so 'cls' is used instead of 'self'
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs  # Additional keyword arguments
    ) -> AsyncResult:
        """
        create_async_generator is a class method that creates an asynchronous generator for the GptTalkRu API.

        :param model: The model to use for the API request
        :param messages: The messages to send to the API
        :param proxy: The proxy to use for the API request, optional
        :param kwargs: Additional keyword arguments
        :return: An asynchronous result object
        """
        if not model:
            model = "gpt-3.5-turbo"  # Set a default model if not provided

        # Headers for the API request
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://gpttalk.ru",
            "Referer": "https://gpttalk.ru/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }

        async with aiohttp.ClientSession(headers=headers) as session:  # Create an asynchronous session
            data = {
                "model": model,
                "modelType":
