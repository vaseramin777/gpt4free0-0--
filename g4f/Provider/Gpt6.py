from __future__ import annotations  # Allows using class names in type hints before they are defined

import json
from aiohttp import ClientSession  # Asynchronous HTTP client for Python

from ..typing import AsyncResult, Messages  # Custom types for AsyncGeneratorProvider
from .base_provider import AsyncGeneratorProvider  # Base class for asynchronous providers
from .helper import format_prompt  # Helper function for formatting prompts


class Gpt6(AsyncGeneratorProvider):
    """
    GPT-6 provider class that inherits from AsyncGeneratorProvider.
    This class implements the create_async_generator() method to interact with the GPT-6 API.
    """

    url = "https://gpt6.ai"
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
        Creates an asynchronous generator for the GPT-6 API.

        :param model: The model to use for generating responses.
        :param messages: A list of messages to send to the API.
        :param proxy: An optional proxy to use for the request.
        :param kwargs: Additional keyword arguments.
        :return: An asynchronous generator for the API response.
        """
        headers = {
            # Header configuration for the API request
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://gpt6.ai",
            "Connection": "keep-alive",
            "Referer": "https://gpt6.ai/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "TE": "trailers",
        }

        async with ClientSession(headers=headers) as session:  # Create an asynchronous HTTP session
            data = {
                "prompts": messages,  # The list of messages to send to the API
                "geoInfo": {
                    "ip": "100.90.100.222",
                    "hostname": "ip-100-090-100-222.um36.pools.vodafone-ip.de",
                    "city": "Muenchen",
                    "region": "North Rhine-Westphalia",
                    "country": "DE",
                    "loc": "44.0910,5.5827",
                    "org": "AS3209 Vodafone GmbH",
                    "postal": "41507",
                    "timezone": "Europe/Berlin",
                },
                "paid": False,
                "character": {
                    "textContent": "",
                    "id": "52690ad6-22e4-4674-93d4-1784721e9944",
                    "name": "GPT6",
                    "htmlContent
