from __future__ import annotations

import json
import requests
from ...typing import Any, CreateResult
from ..base_provider import AbstractProvider  # Importing necessary modules

class Forefront(AbstractProvider):
    url                   = "https://forefront.com"
    supports_stream       = True
    supports_gpt_35_turbo = True  # Class attributes to define the properties of the Forefront provider

    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        
        json_data = {
            "text"          : messages[-1]["content"],
            "action"        : "noauth",
            "id"            : "",
            "parentId"      : "",
            "workspaceId"   : "",
            "messagePersona": "607e41fe-95be-497e-8e97-010a59b2e2c0",
            "model"         : "gpt-4",
            "messages"      : messages[:-1] if len(messages) > 1 else [],
            "internetMode"  : "auto",
        }  # Prepare the JSON data to be sent to the Forefront API

        response = requests.post("https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat",
            json=json_data, stream=True)  # Send a POST request to the Forefront API

        response.raise_for_status()  # Ensure the request was successful

        for token in response.iter_lines():
            if b"delta" in token:
                yield json.loads(token.decode().split("data: ")[1])["delta"]  # Parse and yield the response tokens
