from __future__ import annotations  # Allows using class name in type hints

import asyncio
import aiohttp
from typing import Any, Dict, List, Union

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider


class Acytoo(AsyncGeneratorProvider):
    """
    Acytoo is a class that implements the AsyncGeneratorProvider interface to provide asynchronous generation of
    completion messages using the Acytoo API.
    """

    url: str = 'https://chat.acytoo.com'
    working: bool = False
    supports_message_history: bool = True
    supports_gpt_35_turbo: bool = True

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Creates an asynchronous generator that yields completion messages from the Acytoo API.

        :param model: The model to use for generating completions.
        :param messages: A list of messages to use as context for the completion.
        :param proxy: An optional proxy to use for the request.
        :param kwargs: Additional keyword arguments to include in the request payload.
        :return: An asynchronous generator that yields completion messages.
        """
        async with aiohttp.ClientSession(headers=_create_header()) as session:
            async with session.post(
                f'{cls.url}/api/completions',
                proxy=proxy,
                json=_create_payload(messages, **kwargs)
            ) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()


def _create_header() -> Dict[str, str]:
    """
    Creates the header for the Acytoo API request.

    :return: A dictionary containing the request headers.
    """
    return {
        'accept': '*/*',
        'content-type': 'application/json',
    }


def _create_payload(messages: Messages, temperature: float = 0.5, **kwargs) -> Dict[str, Union[str
