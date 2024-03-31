from __future__ import annotations  # Allows for forward references of annotations

import requests  # Import the requests library for making HTTP requests

from ...typing import Any, CreateResult, Messages  # Import necessary types
from ..base_provider import AbstractProvider  # Import the abstract provider class

class AiService(AbstractProvider):
    # Initialize the AiService class, which inherits from AbstractProvider
    url = "https://aiservice.vercel.app/"  # The base URL for the AI service
    working = False  # A flag indicating if the service is working
    supports_gpt_35_turbo = True  # A flag indicating if the service supports GPT-3.5-turbo

    @staticmethod
    def create_completion(
        model: str,  # The model to use for the completion
        messages: Messages,  # The messages to generate a completion for
        stream: bool,  # A flag indicating if the completion should be streamed
        **kwargs: Any,  # Additional keyword arguments
    ) -> CreateResult:
        # The create_completion coroutine that generates a completion based on the given messages
        base = (
            "\n".join(
                f"{message['role']}: {message['content']}" for message in messages
            )
            + "\nassistant: "
        )
        headers = {
            "accept": "*/*",  # The acceptable content types for the response
            "content-type": "text/plain;charset=UTF-8",  # The content type of the request
            "sec-fetch-dest": "empty",  # The type of fetch request
            "sec-fetch-mode": "cors",  # The type of CORS request
            "sec-fetch-site": "same-origin",  # The origin of the fetched resource
            "Referer": "https://aiservice.vercel.app/chat",  # The referer header
        }
        data = {"input": base}  # The data to send in the request body
        url = "https://aiservice.vercel.app/api/chat/answer"
