from __future__ import annotations

import os

from .errors   import *
from .models   import Model, ModelUtils, _all_models
from .Provider import AsyncGeneratorProvider, ProviderUtils
from .typing   import Messages, CreateResult, AsyncResult, Union
from .         import debug, version
from .base_provider import BaseRetryProvider, ProviderType

def get_model_and_provider(model    : Union[Model, str], 
                           provider : Union[ProviderType, str, None], 
                           stream   : bool,
                           ignored  : list[str] = None,
                           ignore_working: bool = False,
                           ignore_stream: bool = False) -> tuple[str, ProviderType]:
    """
    Retrieves the model and provider based on input parameters.

    This function first checks if the version_check flag is enabled in debug mode. If yes, it disables the flag and checks the version.
    It then processes the input parameters as follows:
    - If the provider is a string, it tries to convert it to a ProviderType using the ProviderUtils.convert dictionary.
    - If the model is a string, it tries to convert it to a Model using the ModelUtils.convert dictionary.
    - If no provider is specified, it uses the best_provider of the model.
    - If the provider is not working, it raises a ProviderNotWorkingError.
    - If the provider does not support streaming and the stream argument is True, it raises a StreamNotSupportedError.

    Args:
        model (Union[Model, str]): The model to use, either as an object or a string identifier.
        provider (Union[ProviderType, str, None]): The provider to use, either as an object, a string identifier, or None.
        stream (bool): Indicates if the operation should be performed as a stream.
        ignored (list[str], optional): List of provider names to be ignored.
        ignore_working (bool, optional): If True, ignores the working status of the provider.
        ignore_stream (bool, optional): If True, ignores the streaming capability of the provider.

    Returns:
        tuple[str, ProviderType]: A tuple containing the model name and the provider type.

    Raises:
        ProviderNotFoundError: If the provider is not found.
        ModelNotFoundError: If the model is not found.
        ProviderNotWorkingError: If the provider is not working.
        StreamNotSupportedError: If streaming is not supported by the provider.
    """
    if debug.version_check:
        debug.version_check = False
        version.utils.check_version()

    if isinstance(provider, str):
        if provider in ProviderUtils.convert:
            provider = ProviderUtils.convert[provider]
        else:
            raise ProviderNotFoundError(f'Provider not found: {provider}')

    if isinstance(model, str):
        if model in ModelUtils.convert:
            model = ModelUtils.convert[model]

    if not provider:
        if isinstance(model, str):
            raise ModelNotFoundError(f'Model not found: {model}')
        provider = model.best_provider

    if not provider:
        raise ProviderNotFoundError(f'No provider found for model: {model}')

    if isinstance(model, Model):
        model = model.name

    if ignored and isinstance(provider, BaseRetryProvider):
        provider.providers = [p for p in provider.providers if p.__name__ not in ignored]

    if not ignore_working and not provider.working:
        raise ProviderNotWorkingError(f'{provider.__name__} is not working')

    if not ignore_stream and not provider.supports_stream and stream:
        raise StreamNotSupportedError(f'{provider.__name__} does not support "stream" argument')

    if debug.logging:
        if model:
            print(f'Using {provider.__name__} provider and {model} model')
        else:
            print(f'Using {provider.__name__} provider')

    debug.last_provider = provider

    return model, provider

class ChatCompletion:
    @staticmethod
    def create(model    : Union[Model, str],
               messages : Messages,
               provider : Union[ProviderType, str, None] = None,
               stream   : bool = False,
               auth     : Union[str, None] = None,
               ignored  : list[str] = None, 
               ignore_working: bool = False,
               ignore_stream_and_auth: bool = False,
               patch_provider: callable = None,
               **kwargs) -> Union[CreateResult, str]:
        """
        Creates a chat completion using the specified model, provider, and messages.

        This function first retrieves the model and provider using the get_model_and_provider function.
    It then checks if authentication is required and not provided, and raises an AuthenticationRequiredError if yes.
    If auth is provided, it adds it to the kwargs.
    It then checks if the provider supports streaming and if the stream argument is True. If yes, it calls the create_async_generator
    method of the provider. Otherwise, it calls the create_completion method of the provider.

    Args:
        model (Union[Model, str]): The model to use, either as an object or a string identifier.
        messages (Messages): The messages for which the completion is to be created.
        provider (Union[ProviderType, str, None], optional): The provider to use, either as an object, a string identifier, or None.
        stream (bool, optional): Indicates if the operation should be performed as a stream.
        auth (Union[str, None], optional): Authentication token or credentials, if required.
        ignored (list[str], optional): List of provider names to be ignored.
        ignore_working (bool, optional): If True, ignores the working status of the provider.
        ignore_stream_and_auth (bool, optional): If True, ignores the stream and authentication requirement checks.
        patch_provider (callable, optional): Function to modify the provider.
        **kwargs: Additional keyword arguments.

    Returns:
        Union[CreateResult, str]: The result of the chat completion operation.

    Raises:
        AuthenticationRequiredError: If
