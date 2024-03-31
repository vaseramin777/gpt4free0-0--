from __future__ import annotations  # Allows using class variables in type hints

import json
import requests

from ...typing import CreateResult, Messages
from ..base_provider import AbstractProvider

class Raycast(AbstractProvider):
    # Class attributes
    url                     = "https://raycast.com"
    supports_gpt_35_turbo   = True
    supports_gpt_4          = True
    supports_stream         = True
    needs_auth              = True
    working                 = True

    @staticmethod
    def create_completion(
            model: str,  # The model to use for the completion
            messages: Messages,  # The messages to generate the completion from
            stream: bool,  # Whether to stream the completion
            proxy: str = None,  # Optional proxy to use for the request
            **kwargs,  # Additional keyword arguments
    ) -> CreateResult:
        # Get the authentication token from the keyword arguments
        auth = kwargs.get('auth')

        # Set up the headers for the request
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': f'Bearer {auth}',  # Add the authentication token to the headers
            'Content-Type': 'application/json',
            'User-Agent': 'Raycast/0 CFNetwork/1410.0.3 Darwin/22.6.0',
        }

        # Parse the messages into the format required by the Raycast API
        parsed_messages = [
            {'author': message['role'], 'content': {'text': message['content']}}
            for message in messages
        ]

        # Set up the data for the request
        data = {
            "debug": False,
            "locale": "en-CN",
            "messages": parsed_messages,
            "model": model,
            "provider": "openai",
            "source": "ai_chat",
            "system_instruction": "markdown",
            "temperature": 0.5
        }

        # Send the request to the Raycast API
        response = requests.post(
            "https://backend.raycast.com/api/v1/ai/chat_completions",
            headers=headers,
            json=data,
            stream=True,
            proxies={"https": proxy}
        )

        # Iterate over the lines of the response
        for token in response.iter_lines():
            # Check if the line contains a completion token
            if b'data: ' not in token:
                continue

            # Decode the token and extract the completion chunk
            completion_chunk = json.loads(token.decode().replace('data: ', ''))

            # Yield the completion token
            token = completion_chunk['text']
            if token != None:
                yield token
