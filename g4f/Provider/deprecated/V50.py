from __future__ import annotations  # Allows using the class name in the class definition

import uuid  # Used to generate a unique identifier for the user
import requests  # Used to make HTTP requests

from ...typing import Any, CreateResult  # Import Any and CreateResult from the typing module
from ..base_provider import AbstractProvider  # Import AbstractProvider from the base_provider module


class V50(AbstractProvider):
    """
    A class representing a provider for generating completions using the V50 API.

    Inherits from AbstractProvider.
    """

    url = 'https://p5.v50.ltd'  # The base URL for the V50 API
    supports_gpt_35_turbo = True  # Whether this provider supports the GPT-3.5-turbo model
    supports_stream = False  # Whether this provider supports streaming responses
    needs_auth = False  # Whether this provider requires authentication
    working = False  # Whether this provider is currently working (not used in this example)

    @staticmethod
    def create_completion(
            model: str,  # The model to use for the completion
            messages: list[dict[str, str]],  # The messages to use as context for the completion
            stream: bool, **kwargs: Any) -> CreateResult:  # Additional keyword arguments
        """
        Create a completion using the V50 API.

        :param model: The model to use for the completion.
        :param messages: The messages to use as context for the completion.
        :param stream: Whether to stream the response.
        :param kwargs: Additional keyword arguments.
        :return: A generator yielding the completion response.
        """

        conversation = (
            "\n".join(
                f"{message['role']}: {message['content']}" for message in messages
            )
            + "\nassistant: "
        )
        """
        Create a conversation string by joining the messages and adding a newline character.
        """

        payload = {
            "prompt"        : conversation,
            "options"       : {},
            "systemMessage" : ".",
            "temperature"   : kwargs.get("temperature", 0.4),
            "top_p"         : kwargs.get("top_p", 0.4),
            "model"         : model,
            "user"          : str(uuid.uuid4())
        }
        """
        Create a payload dictionary with the required parameters for the V50 API request.
        """

        headers = {
            'authority'         : 'p5.v50.ltd',
            'accept'            : 'application/json, text/plain, */*',
            'accept-language'   : 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type'      : 'application/json',
            'origin'            : 'https://p5.v50.ltd',
            'referer'           : 'https://p5.v50.ltd/',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest'    : 'empty',
            'sec-fetch-mode'    : 'cors',
            'sec-fetch-site'    : 'same-origin',
            'user-agent'        : 'Mozilla/5.0 (Windows NT 10
