from __future__ import annotations

import random
import requests
from ...typing import Any, CreateResult
from ..base_provider import AbstractProvider, format_prompt


class Wuguokai(AbstractProvider):
    """
    Wuguokai is a subclass of AbstractProvider, providing a specific implementation for the Wuguokai API.
    """
    url = 'https://chat.wuguokai.xyz'
    supports_gpt_35_turbo = True
    working = False

    @staticmethod
    def create_completion(
            model: str,
            messages: list[dict[str, str]],
            stream: bool,
            **kwargs: Any,
    ) -> CreateResult:
        """
        create_completion is a static method that sends a POST request to the Wuguokai API and returns the response.

        :param model: The model to be used for the completion.
        :param messages: A list of dictionaries containing messages for the completion.
        :param stream: A boolean indicating if the response should be streamed.
        :param kwargs: Additional keyword arguments.
        :return: A CreateResult object.
        """
        headers = {
            'authority': 'ai-api.wuguokai.xyz',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://chat.wuguokai.xyz',
            'referer': 'https://chat.wuguokai.xyz/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        data = {
            "prompt": format_prompt(messages),
            "options": {},
            "userId": f"#/chat/{random.randint(1,99999999)}",
            "usingContext": True
        }

        response = requests.post(
            "https://ai-api20.wuguokai.xyz/api/chat-process",
            headers=headers,
            timeout=3,
            json=data,
            proxies=kwargs.get('proxy', {}),
        )

        # Split the response text and handle errors
        _split = response.text.split("> 若回答失败请重试或多刷新几次界面后重试")
        if response.status_code != 
