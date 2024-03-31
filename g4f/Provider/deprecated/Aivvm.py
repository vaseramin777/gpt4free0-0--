from __future__ import annotations  # Allows using class name in type hints before it is defined

import requests  # Importing requests library for making HTTP requests
import json  # Importing json library for encoding and decoding JSON data

from ..base_provider import AbstractProvider  # Importing AbstractProvider class from base_provider module
from ...typing import CreateResult, Messages  # Importing CreateResult and Messages types from typing module

# A dictionary containing the available models and their details
models = {
    'gpt-3.5-turbo': {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5'},
    'gpt-3.5-turbo-0613': {'id': 'gpt-3.5-turbo-0613', 'name': 'GPT-3.5-0613'},
    'gpt-3.5-turbo-16k': {'id': 'gpt-3.5-turbo-16k', 'name': 'GPT-3.5-16K'},
    'gpt-3.5-turbo-16k-0613': {'id': 'gpt-3.5-turbo-16k-0613', 'name': 'GPT-3.5-16K-0613'},
    'gpt-4': {'id': 'gpt-4', 'name': 'GPT-4'},
    'gpt-4-0613': {'id': 'gpt-4-0613', 'name': 'GPT-4-0613'},
    'gpt-4-32k': {'id': 'gpt-4-32k', 'name': 'GPT-4-32K'},
    'gpt-4-32k-0613': {'id': 'gpt-4-32k-0613', 'name': 'GPT-4-32K-0613'},
}

class Aivvm(AbstractProvider):  # AIVVM provider class inheriting from AbstractProvider
    url                   = 'https://chat.aivvm.com'  # Base URL for the AIVVM API
    supports_stream       = True  # Indicates if the provider supports streaming responses
    working               = False  # Indicates if the provider is currently working
    supports_gpt_35_turbo = True  # Indicates if the provider supports GPT-3.5-turbo model
    supports_gpt_4        = True  # Indicates if the provider supports GPT-4 model

    @classmethod
    def create_completion(cls,  # Class method for creating a completion using the AIVVM API
        model: str,  # The model to use for the completion
        messages: Messages,  # The messages to use for the completion
        stream: bool,  # Whether to stream the response or not
        **kwargs  # Additional keyword arguments
    ) -> CreateResult:  # The return type is CreateResult
        if not model:  # If the model is not provided, use the default model
            model = "gpt-3.5-turbo"
        elif model not in models:  # If the provided model is not supported, raise a ValueError
            raise ValueError(f"Model is not supported: {model}")

        json_data = {  # Prepare the JSON data to send in the request
            "model"       : models[model],  # The selected model
            "messages"    : messages,  # The messages for the completion
            "key"         : "",  # The API key (not used in this example)
            "prompt"      : kwargs.get("system_message", "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."),  # The system message or the provided one
            "temperature" : kwargs.get("temperature", 0.7)  # The temperature or the provided one
        }

        data = json.dumps(json_data)  # Encode the JSON data as a string

        headers = {  # Prepare the headers for the request
            "accept"            : "text/event-stream",  # The accepted response format
            "accept-language"   : "en-US,en;q=0.9",  # The accepted languages
            "content-type"      : "application/json",  # The content type of the request
            "content-length"    : str(len(data)),  # The length of the request data
            "sec-ch-ua"         : "\"Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",  # The user agent
