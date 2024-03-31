from __future__ import annotations

import time  # Import time module for sleep function
import json  # Import json module for json manipulation

from ...typing import CreateResult, Messages  # Import required types
from ..base_provider import AbstractProvider  # Import AbstractProvider base class
from ..helper import format_prompt  # Import format_prompt utility function
from ...webdriver import WebDriver, WebDriverSession, bypass_cloudflare  # Import webdriver-related modules and functions

class MyShell(AbstractProvider):
    # Subclass AbstractProvider for custom provider implementation

    url = "https://app.myshell.ai/chat"  # The URL for the API endpoint
    working = True  # Flag to indicate if the provider is working
    supports_gpt_35_turbo = True  # Flag to indicate if the provider supports GPT-3.5-turbo model
    supports_stream = True  # Flag to indicate if the provider supports streaming responses

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
    ) -> CreateResult:
        # Class method to create a completion using the provider
        with WebDriverSession(webdriver, "", proxy=proxy) as driver:
            # Create a WebDriverSession with the provided webdriver, proxy, and timeout
            bypass_cloudflare(driver, cls.url, timeout)
            # Bypass Cloudflare protection on the API endpoint

            # Prepare the request data
            data = {
                "botId": "4738",
                "conversation_scenario": 3,
                "message": format_prompt(messages),
                "messageType": 1
            }

            # Send the request and handle the response
            script = """
            response = await fetch("https://api.myshell.ai/v1/bot/chat/send_message", {
                "headers": {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "myshell-service-name": "organics-api",
                    "visitor-id": localStorage.getItem("mix_visitorId")
                },
                "body": '{body}',
                "method": "POST"
            })
            window._reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
            """
            driver.execute_script(script.replace("{body}", json.dumps(data)))
            # Execute JavaScript code to send the request and get a reader for the response

            script = """
            chunk = await window._reader.read();
            if (chunk.done) {
                return null;
            }
            content = '';
            chunk.value.split('\\n').forEach((line, index) => {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.substring('data: '.length));
                        if ('content' in data) {
                            content += data['content'];
                        }
                    } catch(e) {}
                 }
            });
            return content;
            """

            # Read and parse the response in chunks
            while True:
                chunk = driver.execute_script(script)
                if chunk:
                    # Yield the parsed chunk if it's not empty
                    yield chunk
                elif chunk != "":
                    # Break the loop if the chunk is empty
                    break
                else:
                    # Sleep for a short duration before
