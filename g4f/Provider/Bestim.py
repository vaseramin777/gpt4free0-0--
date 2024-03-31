from __future__         import annotations  # Allows using the type hints in the class definition

from ..typing           import Messages  # Import the Messages type from the typing module
from .base_provider     import BaseProvider, CreateResult  # Import the base class and the CreateResult type
from ..requests         import get_session_from_browser  # Import the get_session_from_browser function
from uuid               import uuid4  # Import the UUID4 function to generate unique IDs
import requests  # Import the requests library

class Bestim(BaseProvider):  # Define a class named Bestim that inherits from BaseProvider
    url = "https://chatgpt.bestim.org"  # Set the URL for the provider
    supports_gpt_35_turbo = True  # Indicate that this provider supports the GPT-3.5-turbo model
    supports_message_history = True  # Indicate that this provider supports message history
    working = False  # Set the working status to False initially
    supports_stream = True  # Indicate that this provider supports streaming responses

    @classmethod  # Decorate the method as a class method
    def create_completion(  # Define the create_completion class method
        cls,  # Use the class (cls) as the first parameter
        model: str,  # Define the model parameter as a string
        messages: Messages,  # Define the messages parameter as the Messages type
        stream: bool,  # Define the stream parameter as a boolean
        proxy: str = None,  # Define the proxy parameter as an optional string with a default value of None
        **kwargs  # Allow any additional keyword arguments
    ) -> CreateResult:  # Define the return type as CreateResult
        session = get_session_from_browser(cls.url, proxy=proxy)  # Get a session from the browser with the specified URL and proxy

        headers = {  # Define the headers for the request
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'application/json, text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://chatgpt.bestim.org/chat/',
            'Origin': 'https://chatgpt.bestim.org',
            'Alt-Used': 'chatgpt.bestim.org',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }

        data = {  # Define the data for the request
            "messagesHistory": [
                {
                    "id": str(uuid4()),  # Generate a unique ID for each message
                    "content": m["content"],  # Use the content of the message
                    "from": "you" if m["role"] == "user" else "bot"  # Set the 'from' field based on the role of the message
                } for m in messages],
            "type": "chat",
        }

        response = session.post(  # Send a POST request
            url="https://chatgpt.bestim.org
