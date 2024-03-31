from __future__ import annotations

import time
import hashlib

from ...typing import AsyncResult, Messages
from ...requests import StreamSession
from ..base_provider import AsyncGeneratorProvider # Importing necessary modules


class Aibn(AsyncGeneratorProvider):
    url = "https://aibn.cc" # The URL for the AI model
    working = False # Flag to check if the model is currently working
    supports_message_history = True # Flag to check if the model supports message history
    supports_gpt_35_turbo = True # Flag to check if the model supports GPT-3.5-turbo

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            timeout: int = 120,
            **kwargs
    ) -> AsyncResult:
        async with StreamSession(
                impersonate="chrome107",
                proxies={"https": proxy},
                timeout=timeout
        ) as session: # Create a new session with the given parameters
        ...

    def generate_signature(self, timestamp: int, message: str, secret: str = "undefined"):
        """
        Generate a signature for the given data using the SHA-256 algorithm.

        :param timestamp: The current timestamp
        :param message: The message to be signed
        :param secret: The secret key (optional, defaults to "undefined")
        :return: The generated signature
        """
        data = f"{timestamp}:{message}:{secret}"
        return hashlib.sha256(data.encode()).hexdigest()
