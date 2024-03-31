from __future__ import annotations  # Allows using class name in type hints before it's defined

import asyncio
import aiohttp
import hashlib
from typing import AsyncIterable, Dict, List, Optional, Union

# The 'Cromicle' class is an asynchronous generator provider that communicates with the Cromicle API
class Cromicle(AsyncGeneratorProvider):
    url: str = 'https://cromicle.top'  # The base URL for the Cromicle API
    working: bool = False  # A flag indicating if the class is currently working or not
    supports_gpt_35_turbo: bool = True  # A flag indicating if the class supports GPT-3.5-turbo model or not

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: List[Dict[str, Union[str, List[Dict[str, str]]]]],
        proxy: Optional[str] = None,
        **kwargs
    ) -> AsyncIterable[str]:
        """
        Creates an asynchronous generator to generate responses from the Cromicle API.

        :param model: The model to use for the request.
        :param messages: The messages to send to the API.
        :param proxy: The proxy to use for the request.
        :param kwargs: Additional keyword arguments to pass to the 'aiohttp.ClientSession' constructor.
        :return: An asynchronous generator that yields the response stream from the API.
        """
        async with aiohttp.ClientSession(
            headers=_create_header()
        ) as session:
            async with session.post(
                f'{cls.url}/chat',
                proxy=proxy,
                json=_create_payload(format_prompt(messages))
            ) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()


def _create_header() -> Dict[str, str]:
    """
    Creates the header for the Cromicle API request.

    :return: A dictionary containing the header.
    """
    return {
        'accept':
