import ast
import logging
import time
import json
import random
import string
import uvicorn
import nest_asyncio

from fastapi           import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
from typing            import List, Union, Any, Dict, AnyStr
#from ._tokenizer       import tokenize

import g4f
from .. import debug

# Enable logging for debugging purposes
debug.logging = True

class Api:
    def __init__(self, engine: g4f, debug: bool = True, sentry: bool = False,
                 list_ignored_providers: List[str] = None) -> None:
        # Initialize the API with the provided engine, debug settings, and list of ignored providers
        self.engine = engine
        self.debug = debug
        self.sentry = sentry
        self.list_ignored_providers = list_ignored_providers

        self.app = FastAPI()
        nest_asyncio.apply()

        # Define data types for JSON structures
        JSONObject = Dict[AnyStr, Any]
        JSONArray = List[Any]
        JSONStructure = Union[JSONArray, JSONObject]

        # Define the root route for the API
        @self.app.get("/")
        async def read_root():
            return Response(content=json.dumps({"info": "g4f API"}, indent=4), media_type="application/json")

        # Define the /v1 route for the API
        @self.app.get("/v1")
        async def read_root_v1():
            return Response(content=json.dumps({"info": "Go to /v1/chat/completions or /v1/models."}, indent=4), media_type="application/json")

        # Define the /v1/models route for the API
        @self.app.get("/v1/models")
        async def models():
            # Initialize a list to store model information
            model_list = []

            # Iterate over all available models
            for model in g4f.Model.__all__():
                # Get information about the current model
                model_info = (g4f.ModelUtils.convert[model])

                # Add the model information to the list
                model_list.append({
                    'id': model,
                    'object': 'model',
                    'created': 0,
                    'owned_by': model_info.base_provider}
                )

            # Return the list of models as a JSON response
            return Response(content=json.dumps({
                'object': 'list',
                'data': model_list}, indent=4), media_type="application/json")

        # Define the /v1/models/{model_name} route for the API
        @self.app.get("/v1/models/{model_name}")
        async def model_info(model_name: str):
            try:
                # Get information about the specified model
                model_info = (g4f.ModelUtils.convert[model_name])

                # Return the model information as a JSON response
                return Response(content=json.dumps({
                    'id': model_name,
                    'object': 'model',
                    'created': 0,
                    'owned_by': model_info.base_provider
                }, indent=4), media_type="application/json")
            except:
                # If the model does not exist, return an error message
                return Response(content=json.dumps({"error": "The model does not exist."}, indent=4), media_type="application/json")

        # Define the /v1/chat/completions route for the API
        @self.app.post("/v1/chat/completions")
        async def chat_completions(request: Request, item: JSONStructure = None):
            # Initialize a dictionary with default values
            item_data = {
                'model': 'gpt-3.5-turbo',
                'stream': False,
            }

            # If the item parameter is not None, update the item_data dictionary with the
