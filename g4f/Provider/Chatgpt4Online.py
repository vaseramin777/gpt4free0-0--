from __future__ import annotations

import re
import json
from aiohttp import ClientSession

from ..typing import Messages, AsyncResult
from .base_provider import AsyncGeneratorProvider
from .helper import get_random_string

class Chatgpt4Online(AsyncGeneratorProvider):
    """
    A class representing a provider for generating responses from the ChatGPT 4 Online API.
    """
    url = "https://chatgpt4online.org"
    supports_message_history = True  # Whether this provider supports message history
    supports_gpt_35_turbo = True  # Whether this provider supports the GPT-3.5-turbo model
    working = False  # Cloudfare block status
    _wpnonce = None  # Nonce for authentication

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            **kwargs
    ) -> AsyncResult:
        """
        Create an asynchronous generator for generating responses from the ChatGPT 4 Online API.

        :param model: The model to use for generating responses
        :param messages: A list of messages to send to the API
        :param proxy: An optional proxy to use for the request
        :param kwargs: Additional keyword arguments
        :return: An asynchronous generator for generating responses
        """
        headers = {
            "accept": "*/*",
            "accept-language": "en-US",
            "content-type": "application/json",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "referer": "https://chatgpt4online.org/",
            "referrer-policy": "strict-origin-when-cross-origin"
        }

        async with ClientSession(headers=headers) as session:
            if not cls._wpnonce:
                async with session.get(f"{cls.url}/", proxy=proxy) as response:
                    response.raise_for_status()  # Raise an exception if the response status code is not 2xx
                    response = await response.text()  # Read the response body as text
                    result = re.search(r'restNonce&quot;:&quot;(.*?)&quot;', response)  # Search for the nonce in the response
                    if result:
                        cls._wpnonce = result.group(1)  # Set the nonce
                    else:
                        raise RuntimeError("No nonce found")  # Raise an exception if no nonce was found
            data = {
                "botId": "default",
                "customId": None,
                "session": "N/A",
                "chatId": get_random_string(11),  # Generate a random chat ID
                "contextId": 58,
                "messages": messages[:-1],  # Exclude the last message
                "newMessage": messages[-1]["content"],  # Get the content of the last message
                "newImageId": None,
                "stream": True
            }
            async with session.post(
                    f"{cls.url}/wp-json/mwai-ui/v1/chats/submit",
                    json=data,
                    proxy=proxy,
                    headers={"x-wp-nonce": cls._wpnonce}
            ) as response:
                response.raise_for_status()  # Raise an exception if the response status code is not 2xx
                async for line in response.content:
                    if line.startswith(b"data: "):
                        line = json.loads(line[6:])  # Decode the JSON-encoded line
                        if "type" not in line:
                            raise RuntimeError(f"Response: {line}")  # Raise an exception if the response is invalid
                        elif line["type"] == "live":
                            yield line["data"]  # Yield the data if the response is live
                        elif line["type"] == "end":
                            break  # Break the loop if the response is an end message
