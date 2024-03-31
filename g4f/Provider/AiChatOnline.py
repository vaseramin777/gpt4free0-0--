from __future__ import annotations

import json
from aiohttp import ClientSession

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider
from .helper import get_random_string

class AiChatOnline(AsyncGeneratorProvider):
    """
    A class representing an asynchronous generator provider for AiChatOnline.

    Attributes:
        url (str): The base URL for AiChatOnline.
        working (bool): A flag indicating if the provider is working.
        supports_gpt_35_turbo (bool): A flag indicating if the provider supports GPT-35-turbo.
        supports_message_history (bool): A flag indicating if the provider supports message history.
    """

    url = "https://aichatonline.org"
    working = True
    supports_gpt_35_turbo = True
    supports_message_history = False

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Create an asynchronous generator for AiChatOnline.

        Args:
            model (str): The model to use.
            messages (Messages): The messages to send.
            proxy (str, optional): The proxy to use. Defaults to None.

        Returns:
            AsyncResult: An asynchronous result object.
        """
        headers = {
            # A User-Agent header is used to identify the client.
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            # The Accept header indicates the format of the response expected.
            "Accept": "text/event-stream",
            # The Accept-Language header indicates the preferred language.
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            # The Accept-Encoding header indicates the preferred encoding.
            "Accept-Encoding": "gzip, deflate, br",
            # The Referer header indicates the URL of the previous page.
            "Referer": f"{cls.url}/chatgpt/chat/",
            # The Content-Type header indicates the format of the request body.
            "Content-Type": "application/json",
            # The Origin header indicates the origin of the request.
            "Origin": cls.url,
            # The Alt-Used header indicates the alternative DNS name used.
            "Alt-Used": "aichatonline.org",
            # The Connection header indicates the type of connection.
            "Connection": "keep-alive",
            # The Sec-Fetch-Dest header indicates the type of resource being requested.
            "Sec-Fetch-Dest": "empty",
            # The Sec-Fetch-Mode header indicates the type of request.
            "Sec-Fetch-Mode": "cors",
            # The Sec-Fetch-Site header indicates the relationship of the origin to the requested origin.
            "Sec-Fetch-Site": "same-origin",
            # The TE header indicates the trailers that the client is willing to accept.
            "TE": "trailers"
        }

        # Create a new aiohttp ClientSession.
        async with ClientSession(headers=headers) as session:
            data = {
                "botId": "default",
                "customId": None,
                "session": get_random_string(1
