from __future__ import annotations  # Allows using class names in type hints before they are defined

import uuid  # Used to generate unique conversation IDs

from aiohttp import ClientSession, BaseConnector  # Asynchronous HTTP client for making requests

from ..typing import AsyncResult, Messages  # Typing definitions for asynchronous generator and messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin  # Base classes for asynchronous generator providers
from .helper import get_connector  # Helper function to get a connector instance

# Dictionary of available models with their details
models = {
    "gpt-4": {
        "id": "gpt-4",
        "name": "GPT-4",
        "maxLength": 24000,
        "tokenLimit": 8000,
    },
    # ... other models ...
}

class Liaobots(AsyncGeneratorProvider, ProviderModelMixin):
    # Base URL for the Liaobots API
    url = "https://liaobots.site"
    # Flag to track if the provider is working
    working = True
    # Flags to track support for specific features
    supports_message_history = True
    supports_gpt_35_turbo = True
    supports_gpt_4 = True
    # Default model for the provider
    default_model = "gpt-3.5-turbo"
    # List of available models
    models = [m for m in models]
    # Model aliases for mapping custom names to actual model names
    model_aliases = {
        "claude-v2": "claude-2"
    }
    # Auth code and cookie jar for authentication
    _auth_code = None
    _cookie_jar = None

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            auth: str = None,
            proxy: str = None,
            connector: BaseConnector = None,
            **kwargs
    ) -> AsyncResult:
        # Headers for the API requests
        headers = {
            "authority": "liaobots.com",
            "content-type": "application/json",
            "origin": cls.url,
            "referer": f"{cls.url}/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        # Create an asynchronous context manager for the ClientSession
        async with ClientSession(
                headers=headers,
                cookie_jar=cls._cookie_jar,
                connector=get_connector(connector, proxy)
        ) as session:
            # Set the auth code if provided
            cls._auth_code = auth if isinstance(auth, str) else cls._auth_code
            # If no auth code is set, log in and get the auth code
            if not cls._auth_code:
                # Make a POST request to the recaptcha API endpoint
                async with session.post(
                        "https://liaobots.work/recaptcha/api/login",
                        proxy=proxy,
                        data={"token": "abcdefghijklmnopqrst"},
                        verify_ssl=False
                ) as response:
                    # Ensure the request was successful
                    response.raise_for_status()
                # Make a POST request to the user API endpoint
                async with session.post(
                        "https://liaobots.work/api/user",
                        proxy=proxy,
                        json={"authcode": ""},
                        verify_ssl=False
                ) as response:
                    # Ensure the request was successful
                    response.raise_for_status()
                    # Get the auth code from the response JSON
                    cls._auth_code = (await response.json(content_type=None))["authCode"]
                    # Set the cookie jar for future requests
                    cls._cookie_jar = session.cookie_jar
            
            # Prepare the data for the API request
            data = {
                "conversationId": str(uuid.uuid4()),
                "model": models[cls.get_model(model)],
                "messages": messages,
                "key": "",
                "prompt": kwargs.get("system_message", "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully."),
            }
            # Make a POST request to the chat API endpoint
            async with session.post(
                    "https://liaobots.work/api/chat",
                    proxy=proxy,
                    json=data,
                    headers={"x-auth-code": cls._auth_code},
                    verify_ssl=False
            ) as response:
                # Ensure the request was successful
                response.raise_for_status()
                # Create an asynchronous generator to yield chunks of the response content
                async for chunk in response.content.iter_any():
                    # Check if the chunk contains the specific HTML string, indicating an invalid session
                    if b"<html coupert-item=" in chunk:
                        # Raise a runtime error if the invalid session string is detected
                        raise RuntimeError("Invalid session")
                    # If the chunk is not empty, yield its decoded content
                    if chunk:
                        yield chunk.decode()
