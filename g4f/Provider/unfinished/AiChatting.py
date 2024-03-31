from __future__ import annotations

from urllib.parse import unquote

from ...typing import AsyncResult, Messages
from ..base_provider import AbstractProvider
from ...webdriver import WebDriver
from ...requests import Session, get_session_from_browser

class AiChatting(AbstractProvider):
    """
    A class representing the AiChatting provider, which supports GPT-3.5-turbo model.
    """
    url = "https://www.aichatting.net"
    supports_gpt_35_turbo = True
    _session: Session = None  # Session object for making requests

    @classmethod
    def create_completion(
            cls,
            model: str,
            messages: Messages,
            stream: bool,
            proxy: str = None,
            timeout: int = 120,
            webdriver: WebDriver = None,
            **kwargs
    ) -> AsyncResult:
        """
        Create a completion using the AiChatting provider.

        :param model: The model to use for the completion.
        :param messages: The messages to use for the completion.
        :param stream: Whether to stream the response.
        :param proxy: The proxy to use for the request.
        :param timeout: The timeout for the request.
        :param webdriver: The webdriver to use for the request.
        :param kwargs: Additional keyword arguments.
        :return: An asynchronous result object.
        """
        if not cls._session:
            cls._session = get_session_from_browser(cls.url, webdriver, proxy, timeout)

        # Get the visitorId from the session's cookies
        visitorId = unquote(cls._session.cookies.get("aichatting.website.visitorId"))

        headers = {
            "accept": "application/json, text/plain, */*",
            "lang": "en",
            "source": "web"
        }
        data = {
            "roleId": 0,
        }

        try:
            # Create a new conversation with the AiChatting API
            response = cls._session.post("https://aga-api.aichatting.net/aigc/chat/record/conversation/create", json=data, headers=headers)
            response.raise_for_status()
            conversation_id = response.json()["data"]["conversationId"]
        except Exception as e:
            # Reset the session if there was an error
            cls.reset()
            raise e

        headers = {
            "authority": "aga-api.aichatting.net",
            "accept": "text/event-stream,application/json, text/event-stream",
            "lang": "en",
            "source": "web",
            "vtoken": visitorId,
        }
        data = {
            "spaceHandle": True,
            "roleId": 0,
            "messages": messages,
            "conversationId": conversation_id,
        }

        # Send a request to the AiChatting API to get the completion
        response = cls._session.post("https://aga-api.aichatting.net/aigc/chat/v2/stream", json=data, headers=headers, stream=True)
        response.raise_for_status()

        # Stream the response
        for chunk in response.iter_lines():
            if chunk.startswith(b"data:"):
                yield chunk[5:].decode().replace("-=- --", " ").replace("-=-n--", "\n").replace("--@DONE@--", "")

    @classmethod
    def reset(cls):
        """
        Reset the session object.
       
