from __future__ import annotations  # Allows for forward references of annotations

from ...typing import Messages  # Import Messages type from ...typing module
from ..base_provider import AsyncProvider, format_prompt  # Import AsyncProvider and format_prompt from base_provider module
from ..helper import get_cookies  # Import get_cookies from helper module
from ...requests import StreamSession  # Import StreamSession from requests module

class Aichat(AsyncProvider):  # Define a new class Aichat that inherits from AsyncProvider
    url = "https://chat-gpt.org/chat"  # Set the url attribute
    working = False  # Set the working attribute
    supports_gpt_35_turbo = True  # Set the supports_gpt_35_turbo attribute

    @staticmethod  # Define a static method
    async def create_async(
            model: str,  # The model parameter is a string
            messages: Messages,  # The messages parameter is of type Messages
            proxy: str = None, **kwargs) -> str:  # The proxy parameter is a string and is optional, **kwargs allows for any number of keyword arguments

        cookies = get_cookies('chat-gpt.org') if not kwargs.get('cookies') else kwargs.get('cookies')
        if not cookies:  # If cookies are not present
            raise RuntimeError(
                "g4f.provider.Aichat requires cookies, [refresh https://chat-gpt.org on chrome]"
            )

        headers = {
            'authority': 'chat-gpt.org',
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'content-type': 'application/json',
            'origin': 'https://chat-gpt.org',
            'referer': 'https://chat-gpt.org/chat',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        async with StreamSession(headers=headers,
                                    cookies=cookies,
                                    timeout=6,
                                    proxies={"https": proxy} if proxy else None,
                                    impersonate="chrome110", verify=False) as session:  # Create a new StreamSession object

            json_data = {
                "message": format_prompt(messages),  # Format the messages using the format_prompt function
                "temperature": kwargs.get('temperature', 0.5),  # Get the temperature from kwargs, default is 0.5
                "presence_penalty": 0,
                "top_p": kwargs.get('top_p', 1),  # Get the top_p from kwargs, default is 1
                "frequency_penalty": 0,
            }

            async with session.post("https://chat-gpt.org/api/text",
                                    json=json_data) as response:  # Send a POST request with json data

                response.raise_for_status()  # Raise an exception if the status code is not 2xx
                result = await response.json()  # Parse the response as JSON

               
