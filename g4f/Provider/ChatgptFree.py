from __future__ import annotations  # Allows using class name in type hints within the class

import re  # Regular expressions module

from ..requests import StreamSession  # Asynchronous HTTP requests
from ..typing import Messages  # Type hint for messages
from .base_provider import AsyncProvider  # Base asynchronous provider class
from .helper import format_prompt, get_cookies  # Helper functions

class ChatgptFree(AsyncProvider):
    # ChatGPT Free provider class
    url = "https://chatgptfree.ai"  # Base URL for the provider
    supports_gpt_35_turbo = True  # Indicates if the provider supports GPT-3.5-turbo model
    working = False  # Indicates if the provider is currently working
    _post_id = None  # Post ID for the provider
    _nonce = None  # Nonce for the provider

    @classmethod
    async def create_async(
            cls,
            model: str,  # Model name
            messages: Messages,  # Messages to send
            proxy: str = None,  # Proxy to use
            timeout: int = 120,  # Timeout for the request
            cookies: dict = None,  # Cookies to use
            **kwargs  # Additional keyword arguments
    ) -> str:
        # Create an asynchronous provider instance

        if not cookies:
            cookies = get_cookies('chatgptfree.ai')
        if not cookies:
            raise RuntimeError(f"g4f.provider.{cls.__name__} requires cookies [refresh https://chatgptfree.ai on chrome]")

        headers = {
            'authority': 'chatgptfree.ai',
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'origin': 'https://chatgptfree.ai',
            'referer': 'https://chatgptfree.ai/chat/',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        async with StreamSession(
                headers=headers,
                cookies=cookies,
                impersonate="chrome107",
                proxies={"https": proxy},
                timeout=timeout
            ) as session:
            
            if not cls._nonce:
                async with session.get(f"{cls.url}/") as response:
                    
                    response.raise_for_status()
                    response = await response.text()

                    result = re.search(r'data-post-id="([0-9]+)"', response)
                    if not result:
                        raise RuntimeError("No post id found")
                    cls._post_id = result.group(1)

                    result = re.search(r'data-nonce="(.*?)"', response)
                    if result:
                        cls._nonce = result.group(1)

                    else:
                        raise RuntimeError("No nonce found")

            prompt = format_prompt(messages)
            data = {
                "_wpnonce": cls._nonce,
                "post_id": cls._post_id,
                "url": cls.url,
                "action": "wpaicg_chat_shortcode_message",
                "message": prompt,
                "bot_id": "0"
            }
            async with session.post(f"{cls.url}/wp-admin/admin-ajax.php", data=data, cookies=cookies) as response:

                response.raise_for_status()
                return (await response.json())["data"]
