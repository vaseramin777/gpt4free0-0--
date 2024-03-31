from __future__ import annotations  # Allows using class name in type hints within the class

import json
from typing import AsyncResult, Messages  # Importing custom types

import aiohttp  # Asynchronous HTTP client
from ...typing import AsyncResult, Messages  # Importing custom types
from ..base_provider import AsyncGeneratorProvider  # Base class for asynchronous generators
from ..helper import format_prompt, get_cookies  # Helper functions

class OpenAssistant(AsyncGeneratorProvider):
    # Class variables
    url = "https://open-assistant.io/chat"
    needs_auth = True
    working = False
    model = "OA_SFT_Llama_30B_6"

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            cookies: dict = None,
            **kwargs
    ) -> AsyncResult:
        # Get cookies if not provided
        if not cookies:
            cookies = get_cookies("open-assistant.io")

        # Set up headers for the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

        # Create an asynchronous context manager for the ClientSession
        async with aiohttp.ClientSession(
                cookies=cookies,
                headers=headers
        ) as session:
            # Create a chat ID by sending a POST request
            async with session.post("https://open-assistant.io/api/chat", proxy=proxy) as response:
                chat_id = (await response.json())["id"]

            # Prepare data for the next POST request
            data = {
                "chat_id": chat_id,
                "content": f" [INST]\n{format_prompt(messages)}\n[/INST]",
                "parent_id": None
            }

            # Create a parent ID by sending a POST request
            async with session.post("https://open-assistant.io/api/chat/prompter_message", proxy=proxy, json=data) as response:
                parent_id = (await response.json())["id"]

            # Prepare data for the next POST request
            data = {
                "chat_id": chat_id,
                "parent_id": parent_id,
                "model_config_name": model if model else cls.model,
                "sampling_parameters":{
                    "top_k": 50,
                    "top_p": None,
                    "typical_p": None,
                    "temperature": 0.35,
                    "repetition_penalty": 1.1111111111111112,
                    "max_new_tokens": 1024,
                    **kwargs
                },
                "plugins":[]
            }

            # Send a POST request to get the assistant message
            async with session.post("https://open-assistant.io/api/chat/assistant_message", proxy=proxy, json=data) as response:
                data = await response.json()

                # Extract the message ID from the response
                if "id" in data:
                    message_id = data["id"]
                elif "message" in data:
                    # Raise a runtime error if there's an error message
                    raise RuntimeError(data["message"])
                else:
                    # Raise an exception if the response status is not 200
                    response.raise_for_status()

            # Prepare parameters for the next POST request
            params = {
                'chat_id': chat_id,
                'message_id': message_id,
            }

            # Send a POST request to get the generated text
            async with session.post("https://open-assistant.io/api/chat/events", proxy=proxy, params=params) as response:
                # Decode the response content to a string
                start = "data: "
                async for line in response.content:
                    line = line.decode("utf-8")
                    # Yield the text if the line starts with the "data: " prefix
                    if line and line.startswith(start):
                        line = json.loads(line[len(start):])
                        if line["event_type"] == "token":
                            yield line["text"]

            # Prepare parameters for the next DELETE request
            params = {
                'chat_id': chat_id,
            }

            # Delete the chat by sending a DELETE request
            async with session.delete("https://open-assistant.io/api/chat", proxy=proxy, params=params) as response:
                # Raise an exception if the response status is not 200
                response.raise_for_status()
