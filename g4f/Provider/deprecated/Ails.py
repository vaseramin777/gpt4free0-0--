from __future__ import annotations  # Allows using class names in type hints before they are defined

import hashlib
import time
import uuid
import json
from datetime import datetime
from aiohttp import ClientSession  # Asynchronous HTTP client for Python

from ...typing import SHA256, AsyncResult, Messages  # Custom types
from ..base_provider import AsyncGeneratorProvider  # Base class for asynchronous generator providers

class Ails(AsyncGeneratorProvider):
    # Class for providing asynchronous text generation using the AILS API

    url = "https://ai.ls"  # Base URL for the AILS API
    working = False  # Flag to indicate if the provider is currently working
    supports_message_history = True  # Flag to indicate if the provider supports message history
    supports_gpt_35_turbo = True  # Flag to indicate if the provider supports the GPT-3.5-turbo model

    @staticmethod
    async def create_async_generator(
        model: str,  # Model to use for text generation
        messages: Messages,  # List of messages to generate a response for
        stream: bool,  # Flag to indicate if the response should be streamed
        proxy: str = None,  # Proxy to use for the HTTP request
        **kwargs  # Additional keyword arguments
    ) -> AsyncResult:
        # Creates an asynchronous generator for text generation

        headers = {
            # Request headers
            # ...
        }

        async with ClientSession(
                headers=headers
            ) as session:
            # Creates an asynchronous HTTP client session

            timestamp = _format_timestamp(int(time.time() * 1000))
            # Formats the current timestamp

            json_data = {
                # Request data
                # ...
            }

            async with session.post(
                        "https://api.caipacity.com/v1/chat/completions",
                        proxy=proxy,
                        json=json_data
                    ) as response:
                # Sends a POST request to the AILS API

                response.raise_for_status()
                # Raises an exception if the request was not successful

                start = "data: "
                async for line in response.content:
                    # Iterates over the response content line by line

                    line = line.decode('utf-8')
                    if line.startswith(start) and line != "data: [DONE]":
                        # Processes the line if it starts with "data: " and is not "[DONE]"

                        line = line[len(start):-1]
                        line = json.loads(line)
                        # Decodes and parses the line as JSON

                        token = line["choices"][0]["delta"].get("content")
                        # Extracts the generated token from the JSON data

                        if token:
                            if "ai.ls" in token or "ai.ci" in token:
                                # Raises an exception if the generated token contains certain keywords
                                raise Exception(f"Response Error: {token}")
                            yield token
                            # Yields the generated token

def _hash(json_data: dict[str, str]) -> SHA256:
    # Generates a SHA-256 hash of the input data

    base_string: str = f'{json_data["t"]}:{json_data["m"]}:WI,2rU#_r:r~aF4aJ36[.Z(/8Rv93Rf:{len(json_data["m"])}'
    # Constructs the base string for the hash

    return SHA256(hashlib.sha256(base_string.encode()).hexdigest())
    # Returns the SHA-256 hash of the base string

def _format_timestamp(timestamp: int) -> str:
    # Formats the input timestamp as a string

    e = timestamp
    n = e % 10
    r = n + 1 if n % 2 == 0 else n
    return str(e - n + r)
    # Returns the formatted timestamp
