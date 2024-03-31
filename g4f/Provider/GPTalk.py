from __future__ import annotations  # Allows using class name in type hints before it's defined

import secrets  # For generating random data
import time     # For getting the current timestamp
import json     # For working with JSON data
from aiohttp import ClientSession  # For making asynchronous HTTP requests

from ..typing import AsyncResult, Messages  # Importing custom types
from .base_provider import AsyncGeneratorProvider  # Importing base class
from .helper import format_prompt  # Importing helper function

class GPTalk(AsyncGeneratorProvider):
    # Class representing a GPTalk provider for generating responses asynchronously

    url = "https://gptalk.net"  # Base URL for GPTalk API
    working = True  # Flag indicating if the provider is working or not
    supports_gpt_35_turbo = True  # Flag indicating if the provider supports GPT-3.5-turbo model
    _auth = None  # Authentication data
    used_times = 0  # Number of times the provider has been used

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            **kwargs
    ) -> AsyncResult:
        # Factory method for creating an asynchronous generator

        if not model:
            # If no model is provided, use the default one
            model = "gpt-3.5-turbo"

        timestamp = int(time.time())  # Getting the current timestamp

        headers = {
            'authority': 'gptalk.net',
            # ... other headers ...
            'x-auth-timestamp': f"{timestamp}",  # Sending the current timestamp in headers
        }

        async with ClientSession(headers=headers) as session:
            if not cls._auth or cls._auth["expires_at"] < timestamp or cls.used_times == 5:
                # If authentication data is not set or expired, or the provider has been used 5 times,
                # generate new authentication data

                data = {
                    "fingerprint": secrets.token_hex(16).zfill(32),  # Generating a random fingerprint
                    "platform": "fingerprint"
                }

                async with session.post(f"{cls.url}/api/chatgpt/user/login", json=data, proxy=proxy) as response:
                    # Sending a login request to the GPTalk API

                    response.raise_for_status()  # Raise an exception if the request failed

                    cls._auth = (await response.json())["data"]  # Storing the authentication data

                cls.used_times = 0  # Resetting the used times counter

            data = {
                "content": format_prompt(messages),  # Preparing the prompt data
                "accept": "stream",  # Requesting a stream response
                "from": 1,
                "model": model,
                "is_mobile": 0,
                "user_agent": headers["user-agent"],
                "is_open_ctx": 0,
                "prompt": "",
                "roid": 111,
                "temperature": 0,
                "ctx_msg_count": 3,
                "created_at": timestamp
            }

            headers = {
                'authorization': f'Bearer {cls._auth["token"]}',  # Adding the authentication token to headers
            }

            async with session.post(f"{cls.url}/api/chatgpt/chatapi/text", json=data, headers=headers, proxy=proxy) as response:
                # Sending a request to generate a response

                response.raise_for_status()  # Raise an exception if the request failed

                token = (await response.json())["data"]["token"]  # Extracting the token from the response

                cls.used_times += 1  # Incrementing the used times counter

            last_message = ""  # Initializing the last message variable

            async with session.get(f"{cls.url}/api/chatgpt/chatapi/stream", params={"token": token}, proxy=proxy) as response:
                # Sending a request to get the stream response

                response.raise_for_status()  # Raise an exception if the request failed

                async for line in response.content:
                    # Iterating over the stream response lines

                    if line.startswith(b"data: "):
                        if line.startswith(b"data: [DONE]"):
                            # If the response is marked as done, break the loop
                            break

                        message = json.loads(line[6:-1])["content"]  # Extracting the message content

                        yield message[len(last_message):]  # Yielding the message part without the already processed text

                        last_message = message  # Updating the last message variable
