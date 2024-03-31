from __future__ import annotations  # Allows using class name in type hints

import json
from aiohttp import ClientSession  # Asynchronous HTTP client

from ..typing import AsyncResult, Messages  # Custom types
from .base_provider import AsyncGeneratorProvider  # Base class for asynchronous providers

class Chatxyz(AsyncGeneratorProvider):
    """
    A class representing an asynchronous generator provider for the chat.3211000.xyz API.
    """
    url = "https://chat.3211000.xyz"
    working = True  # Indicates if the provider is currently working
    supports_gpt_35_turbo = True  # Indicates if the provider supports GPT-3.5-turbo model
    supports_message_history = True  # Indicates if the provider supports message history

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            **kwargs
    ) -> AsyncResult:
        """
        Creates an asynchronous generator for the chat.3211000.xyz API.

        :param model: The model to use for the API request
        :param messages: The messages to send to the API
        :param proxy: The proxy to use for the API request, optional
        :param kwargs: Additional keyword arguments for the API request
        :return: An asynchronous generator
        """
        headers = {
            'Accept': 'text/event-stream',  # Accepts event stream response
            'Accept-Encoding': 'gzip, deflate, br',  # Accepts compressed response
            'Accept-Language': 'en-US,en;q=0.5',  # Accepts English language
            'Alt-Used': 'chat.3211000.xyz',  # Alternate host name
            'Content-Type': 'application/json',  # Sends JSON data
            'Host': 'chat.3211000.xyz',  # Host name
            'Origin': 'https://chat.3211000.xyz',  # Origin of the request
            'Referer': 'https://chat.3211000.xyz/',  # Referer of the request
            'Sec-Fetch-Dest': 'empty',  # Destination of the request
            'Sec-Fetch-Mode': 'cors',  # Request uses CORS
            'Sec-Fetch-Site': 'same-origin',  # Site of the request
            'TE': 'trailers',  # Indicates that the client can handle trailers
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',  # User agent
            'x-requested-with': 'XMLHttpRequest'  # Indicates that the request is XMLHttpRequest
        }

        async with ClientSession(headers=headers) as session:  # Creates a new asynchronous session
            data = {
                "messages": messages,  # The messages to send to the API
                "stream": True,  # Indicates that the response should be streamed
                "model": "gpt-3.5-turbo",  # The model to use for the API request
                "temperature": 0.5,  # Temperature parameter for the API request
                "presence_penalty": 0,  # Presence penalty parameter for the API request
                "frequency_penalty": 0,  # Frequency penalty parameter
