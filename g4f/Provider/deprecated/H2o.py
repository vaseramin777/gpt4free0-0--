from __future__ import annotations

import json
import uuid

import aiohttp  # Async HTTP client for Python

from ...typing import AsyncResult, Messages  # Custom types
from ..base_provider import AsyncGeneratorProvider, format_prompt  # Base class and utility function

class H2o(AsyncGeneratorProvider):
    """
    H2o is an asynchronous generator provider that communicates with the H2O AI GPT-G model.
    It sends messages to the model and yields the generated tokens one by one.
    """
    url = "https://gpt-gm.h2o.ai"
    model = "h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1"

    @classmethod
    async def create_async_generator(
            cls,
            model: str = None,  # Model name (optional)
            messages: Messages,  # List of messages
            proxy: str = None,  # Proxy URL (optional)
            **kwargs  # Additional parameters
    ) -> AsyncResult:
        """
        Create an asynchronous generator for the H2o class.

        :param model: Model name (optional, defaults to the class-level model)
        :param messages: List of messages
        :param proxy: Proxy URL (optional)
        :param kwargs: Additional parameters
        :return: Asynchronous generator
        """
        model = model if model else cls.model
        headers = {"Referer": f"{cls.url}/"}

        async with aiohttp.ClientSession(
                headers=headers
        ) as session:  # Create an HTTP client session
            # Set up the conversation with the model
            await cls._setup_conversation(session, model, proxy)

            # Send the input messages and yield the generated tokens
            data = {
                "inputs": format_prompt(messages),
                "parameters": {
                    "temperature": 0.4,
                    "truncate": 2048,
                    "max_new_tokens": 1024,
                    "do_sample": True,
                    "repetition_penalty": 1.2,
                    "return_full_text": False,
                    **kwargs
                },
                "stream": True,
                "options": {
                    "id": str(uuid.uuid4()),
                    "response_id": str(uuid.uuid4()),
                    "is_retry": False,
                    "use_cache": False,
                    "web_search_id": "",
                },
            }
            async with session.post(
                    f"{cls.url}/conversation/{conversationId}",
                    proxy=proxy,
                    json=data
            ) as response:
                start = "data:"
                async for line in response.content:
                    line = line.decode("utf-8")
                    if line and line.startswith(start):
                        line = json.loads(line[len(start):-1])
                        if not line["token"]["special"]:
                            yield line["token"]["text"]

            # Clean up the conversation
            await cls._cleanup_conversation(session, conversationId, proxy)

    @staticmethod
    async def _setup_conversation(
            session: aiohttp.ClientSession,
            model: str,
            proxy: str = None
    ):
        """
        Set up a conversation with the model.

        :param session: HTTP client session
        :param model: Model name
        :param proxy: Proxy URL (optional)
        """
        data = {
            "ethicsModalAccepted": "true",
            "shareConversationsWithModelAuthors": "true",
            "ethicsModalAcceptedAt": "",
            "activeModel": model,
            "searchEnabled": "true",
        }
        async with session.post(
                f"{cls.url}/settings",
                proxy=proxy,
                data=data
        ) as response:
            response.raise_for_status()

        async with session.post(
                f"{cls.url}/conversation",
                proxy=proxy,
                json={"model": model},
        ) as response:
            response.raise_for_status()
            conversationId = (await response.json())["conversationId"]

    @staticmethod
    async def _cleanup_conversation(
            session: aiohttp.ClientSession,
            conversationId: str,
            proxy: str = None
    ):
        """
        Clean up the conversation.

        :param session: HTTP client session
        :param conversationId: Conversation ID
        :param proxy: Proxy URL (optional)
        """
        async with
