from __future__ import annotations

import asyncio
import proxy
from aiohttp import ClientSession
from typing import Any, Dict, List, Optional, Union

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider

class AiAsk(AsyncGeneratorProvider):
    # The URL for the AI service
    url = "https://e.aiask.me"
    
    # Indicates if the provider supports message history
    supports_message_history = True
    
    # Indicates if the provider supports GPT-3.5-turbo model
    supports_gpt_35_turbo = True
    
    # Indicates if the provider is currently working
    working = False

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        **kwargs
    ) -> AsyncResult:
        # Define the headers for the request
        headers = {
            "accept": "application/json, text/plain, */*",
            "origin": cls.url,
            "referer": f"{cls.url}/chat",
        }
        
        # Create a new ClientSession with the headers
        async with ClientSession(headers=headers) as session:
            data = {
                "continuous": True,
                "id": "fRMSQtuHl91A4De9cCvKD",
                "list": messages,
                "models": "0",
                "prompt": "",
                "temperature": kwargs.get("temperature", 0.5),
                "title": "",
            }
            
            # Initialize the buffer for the response
            buffer = ""
            
            # Define the rate limit message
            rate_limit = "您的免费额度不够使用这个模型啦，请点击右上角登录继续使用！"
            
            # Send the POST request to the AI service
            async with session.post(f"{cls.url}/v1/chat/gpt/", json=data, proxy=proxy) as response:
                # Check if the response was successful
                response.raise_for_status()
                
                # Iterate over the chunks of the response content
                async for chunk in response.content.iter_any():
                    # Decode the chunk and add it to the buffer
                    buffer += chunk.decode()
                    
                    # Check if the buffer contains the rate limit message
                    if not rate_limit.startswith(buffer):
                        # Yield the
