from __future__ import annotations
import requests, json

from .base_provider import AbstractProvider  # Importing AbstractProvider class
from ..typing       import CreateResult, Messages  # Importing CreateResult and Messages types
from json           import dumps  # Importing dumps function for JSON data formatting

class GeekGpt(AbstractProvider):  # Defining GeekGpt class that inherits from AbstractProvider
    url = 'https://chat.geekgpt.org'  # Base URL for API requests
    working = True  # Flag to check if the provider is working
    supports_message_history = True  # Flag to check if the provider supports message history
    supports_stream = True  # Flag to check if the provider supports streaming responses
    supports_gpt_35_turbo = True  # Flag to check if the provider supports GPT-3.5-turbo model
    supports_gpt_4 = True  # Flag to check if the provider supports GPT-4 model

    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs
    ) -> CreateResult:  # Defining the class method for creating a completion
        if not model:  # If the model is not provided, use the default model
            model = "gpt-3.5-turbo"

        json_data = {
            'messages': messages,  # The messages to generate a completion for
            'model': model,  # The model to use for completion generation
            'temperature': kwargs.get('temperature', 0.9),  # The temperature parameter for controlling randomness
            'presence_penalty': kwargs.get('presence_penalty', 0),  # The presence penalty parameter for avoiding repetition
            'top_p': kwargs.get('top_p', 1),  # The top-p parameter for nucleus sampling
            'frequency_penalty': kwargs.get('frequency_penalty', 0),  # The frequency penalty parameter for avoiding repetition
            'stream': True  # Flag to enable streaming responses
        }

        data = dumps(json_data, separators=(',', ':'))  # Formatting JSON data

        headers = {
            'authority': 'ai.fakeopen.com',  # The authority for the API request
            'accept': '*/*',  # The accepted response types
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',  # The accepted languages
            'authorization': 'Bearer pk-this-is-a-real-free-pool-token-for-everyone',  # The authorization token
            'content-type': 'application/json',  # The content type of the request
            'origin': 'https://chat.geekgpt.org',  # The origin of the request
            'referer': 'https://chat.geekgpt.org/',  # The referer of the request
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',  # The user agent information
            'sec-ch-ua-mobile': '?0',  # Flag to indicate if the request is from a mobile device
            'sec-ch-ua-platform': '"macOS"',  # The platform information
            'sec-fetch-dest': 'empty',  # The destination of the request
            'sec-fetch-mode': 'cors',  # The fetch mode of the request
            'sec-fetch-site': 'cross-site',  # The fetch site of the request
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',  # The user agent information
        }

        response = requests.post("https://ai.fakeopen.com/v1/chat/completions", 
                                 headers=headers, data=data, stream=True)  # Sending the
