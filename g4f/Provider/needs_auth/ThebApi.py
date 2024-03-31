from __future__ import annotations  # Allows using class name in type hints before it's defined

import requests  # Import the requests library for making HTTP requests

from ...typing import Any, CreateResult, Messages  # Import custom types
from ..base_provider import AbstractProvider  # Import the abstract base provider

# Define a dictionary of supported models with their user-friendly names
models = {
    "theb-ai": "TheB.AI",
    "gpt-3.5-turbo": "GPT-3.5",
    "gpt-3.5-turbo-16k": "GPT-3.5-16K",
    "gpt-4-turbo": "GPT-4 Turbo",
    "gpt-4": "GPT-4",
    "gpt-4-32k": "GPT-4 32K",
    "claude-2": "Claude 2",
    "claude-1": "Claude",
    "claude-1-100k": "Claude 100K",
    "claude-instant-1": "Claude Instant",
    "claude-instant-1-100k": "Claude Instant 100K",
    "palm-2": "PaLM 2",
    "palm-2-codey": "Codey",
    "vicuna-13b-v1.5": "Vicuna v1.5 13B",
    "llama-2-7b-chat": "Llama 2 7B",
    "llama-2-13b-chat": "Llama 2 13B",
    "llama-2-70b-chat": "Llama 2 70B",
    "code-llama-7b": "Code Llama 7B",
    "code-llama-13b": "Code Llama 13B",
    "code-llama-34b": "Code Llama 34B",
    "qwen-7b-chat": "Qwen 7B"
}


# Subclass AbstractProvider to create a ThebApi provider
class ThebApi(AbstractProvider):
    url = "https://theb.ai"  # The base URL for the API
    working = True  # A flag indicating if the provider is working or not
    needs_auth = True  # A flag indicating if the provider requires authentication

    @staticmethod
    def create_completion(
        model: str,  # The model to use for the completion
        messages: Messages,  # The messages to generate a completion for
        stream: bool,  # Whether to stream the completion or not
        auth: str,  # The authentication token
        proxy: str = None,  # An optional proxy to use for the request
        **kwargs  # Additional keyword arguments
    ) -> CreateResult:  # The type of the result returned by this method
        if model and model not in models:  # Raise a ValueError if the model is not supported
            raise ValueError(f"Model are not supported: {model}")

        headers = {
            'accept': 'application/json',  # The 'Accept' header for the request
            'authorization': f'Bearer {auth}',  # The 'Authorization' header for the request
            'content-type': 'application/json',  # The 'Content-Type' header for the request
        }

        # Define the request data
        data: dict[str, Any] = {
            "model": model if model else "gpt-3.5-turbo",
            "messages": messages,
            "stream": stream,
            "model_params": {
                "system_prompt": kwargs.get("system_message", "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-3.5 architecture."),
                "temperature": 1,
                "top_p": 1,
                **kwargs
            }
        }

        # Make the API request
        response = requests.post(
            "https://api.theb.ai/v1/chat/completions
