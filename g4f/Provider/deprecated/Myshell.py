# not using WS anymore

from __future__ import annotations

import json, uuid, hashlib, time, random

from aiohttp import ClientSession
from aiohttp.http import WSMsgType
import asyncio

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, format_prompt

# A dictionary that maps model names to their corresponding unique identifiers
models = {
    "samantha": "1e3be7fe89e94a809408b1154a2ee3e1",
    "gpt-3.5-turbo": "8077335db7cd47e29f7de486612cc7fd",
    "gpt-4": "01c8de4fbfc548df903712b0922a4e01",
}


class Myshell(AsyncGeneratorProvider):
    # The base URL for the API
    url = "https://app.myshell.ai/chat"
    # A flag to track if the websocket is currently working
    working               = False
    # Flags to track if the provider supports specific models
    supports_gpt_35_turbo = True
    supports_gpt_4        = True

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            proxy: str = None,
            timeout: int = 90,
            **kwargs
    ) -> AsyncResult:
        """
        The main entry point for creating an async generator.

        :param model: The model to use for generating responses.
        :param messages: A list of messages to send to the model.
        :param proxy: An optional proxy to use for the request.
        :param timeout: The timeout for the request.
        :param kwargs: Additional keyword arguments.
        :return: An async generator.
        """
        if not model:
            bot_id = models["samantha"]
        elif model in models:
            bot_id = models[model]
        else:
            raise ValueError(f"Model are not supported: {model}")

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        visitor_id = generate_visitor_id(user_agent)

        async with ClientSession(
                headers={'User-Agent': user_agent}
        ) as session:
            async with session.ws_connect(
                    "wss://api.myshell.ai/ws/?EIO=4&transport=websocket",
                    autoping=False,
                    timeout=timeout,
                    proxy=proxy
            ) as wss:
                # Send and receive hello message
                await wss.receive_str()
                message = json.dumps({"token": None, "visitorId": visitor_id})
                await wss.send_str(f"40/chat,{message}")
                await wss.receive_str()

                # Fix "need_verify_captcha" issue
                await asyncio.sleep(5)

                # Create chat message
                text = format_prompt(messages)
                chat_data = json.dumps(["text_chat",{
                    "reqId": str(uuid.uuid4()),
                    "botUid": bot_id,
                    "sourceFrom": "myshellWebsite",
                    "text": text,
                    **generate_signature(text)
                }])

                # Send chat message
                chat_start = "42/chat,"
                chat_message = f"{chat_start}{chat_data}"
                await wss.send_str(chat_message)

                # Receive messages
                async for message in wss:
                    if message.type != WSMsgType.TEXT:
                        continue
                    # Ping back
                    if message.data == "2":
                        await wss.send_str("3")
                        continue
                    # Is not chat message
                    if not message.data.startswith(chat_start):
                        continue
                    data_type, data = json.loads(message.data[len(chat_start):])
                    if data_type == "text_stream":
                        if data["data"]["text"]:
                            yield data["data"]["text"]
                        elif data["data"]["isFinal"]:
                            break
                    elif data_type in ("message_replied", "need_verify_captcha"):
                        raise RuntimeError(f"Received unexpected message: {data_type}")


def generate_timestamp() -> str:
    """
    Generates a timestamp string.

    :return: A string representation of the timestamp.
    """
    return str(
        int(
            str(int(time.time() * 1000))[:-1]
            + str(
                sum(
                    2 * int(digit)
                    if idx % 2 == 0
                    else 3 * int(digit)
                    for idx, digit in enumerate(str(int(time.time() * 1000))[:-1])
                )
                % 10
            )
        )
    )

def generate_signature(text: str):
    """
    Generates a signature for the given text.

    :param text: The text to generate a signature for.
    :return: A dictionary containing the signature, timestamp, version, and secret.
    """
    timestamp = generate_timestamp()
    version = 'v1.0.0'
    secret = '8@VXGK3kKHr!u2gA' 
    data = f"{version}#{text}#{timestamp}#{secret}"
    signature = hashlib.md5(data.encode
