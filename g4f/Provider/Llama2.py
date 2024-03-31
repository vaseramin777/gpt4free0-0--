from __future__ import annotations  # Allows using class name in type hints before it's defined

import asyncio
import aiohttp
from typing import Any, Dict, List, Optional, Tuple

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin

class Llama2(AsyncGeneratorProvider, ProviderModelMixin):
    # Class variables
    url = "https://www.llama2.ai"
    working = True
    supports_message_history = True
    default_model = "meta/llama-2-70b-chat"
    models = [
        "meta/llama-2-7b-chat",
        "meta/llama-2-13b-chat",
        "meta/llama-2-70b-chat",
    ]
    model_aliases = {
        "meta-llama/Llama-2-7b-chat-hf": "meta/llama-2-7b-chat",
        "meta-llama/Llama-2-13b-chat-hf": "meta/llama-2-13b-chat",
        "meta-llama/Llama-2-70b-chat-hf": "meta/llama-2-70b-chat",
    }

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        # Headers dictionary is initialized here with default values
        headers = {
            # ...
        }

        async with aiohttp.ClientSession(headers=headers) as session:  # Uses aiohttp.ClientSession to manage HTTP requests
            # ...

            # The response is processed asynchronously here
            async for chunk in response.content.iter_any():
                # ...
                yield chunk.decode(errors="ignore")  # Yields each chunk of the response as a string

def format_prompt(messages: Messages):
    # Formats the prompt by joining the messages with newline characters
    messages = [
        # ...
    ]
    return "\n".join(messages) + "\n"
