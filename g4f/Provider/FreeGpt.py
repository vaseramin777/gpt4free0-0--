from __future__ import annotations  # Allows using class name in type hints before it's defined

import time, hashlib, random  # Import required modules

from ..typing import AsyncResult, Messages  # Import custom types
from ..requests import StreamSession  # Import StreamSession class
from .base_provider import AsyncGeneratorProvider  # Import AsyncGeneratorProvider base class

# Define a list of domains for load balancing or failover
domains = [
    'https://s.aifree.site'
]

class FreeGpt(AsyncGeneratorProvider):
    """
    FreeGpt class implementing AsyncGeneratorProvider to provide GPT-3.5-turbo model functionality.
    """
    url = "https://freegpts1.aifree.site/"  # Base URL for API requests
    working = False  # Flag to track if the provider is currently working
    supports_message_history = True  # Flag indicating support for message history
    supports_gpt_35_turbo = True  # Flag indicating support for GPT-3.5-turbo model

    @classmethod
    async def create_async_generator(  # Class method to create an async generator
        cls,
        model: str,  # Model name
        messages: Messages,  # List of messages
        proxy: str = None,  # Optional proxy string
        timeout: int = 120,  # Timeout in seconds
        **kwargs  # Additional keyword arguments
    ) -> AsyncResult:
        """
        create_async_generator method to create an async generator for the GPT-3.5-turbo model.

        :param model: Model name
        :param messages: List of messages
        :param proxy: Optional proxy string
        :param timeout: Timeout in seconds
        :param kwargs: Additional keyword arguments
        :return: AsyncResult
        """
        async with StreamSession(  # Create a new StreamSession instance
            impersonate="chrome107",  # Impersonate Chrome 107
            timeout=timeout,  # Set timeout
            proxies={"https": proxy}  # Set proxy if provided
        ) as session:
            prompt = messages[-1]["content"]  # Get the last message as the prompt
            timestamp = int(time.time())  # Get the current timestamp
            data = {
                "messages": messages,  # Pass the messages list
                "time": timestamp,  # Pass the timestamp
                "pass": None,  # Placeholder for password (not used)
                "sign": generate_signature(timestamp, prompt)  # Generate the signature
            }
            url = random.choice(domains)  # Choose a random domain from the list
            async with session.post(f"{url}/api/generate", json=
