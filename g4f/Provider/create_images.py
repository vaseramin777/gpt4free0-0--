from __future__ import annotations

import re
import asyncio
from .. import debug
from ..typing import CreateResult, Messages
from ..base_provider import BaseProvider, ProviderType

# system_message:
# A string containing a message that explains the image creation capability.
# This message will be prefixed to messages.
system_message = """
You can generate custom images with the DALL-E 3 image generator.
To generate an image with a prompt, do this:
<img data-prompt="keywords for the image">
Don't use images with data uri. It is important to use a prompt instead.
<img data-prompt="image caption">
"""

class CreateImagesProvider(BaseProvider):
    """
    Provider class for creating images based on text prompts.

    This provider handles image creation requests embedded within message content,
    using provided image creation functions.

    Attributes:
        provider (ProviderType): The underlying provider to handle non-image related tasks.
        create_images (callable): A function to create images synchronously.
        create_images_async (callable): A function to create images asynchronously.
        system_message (str): A message that explains the image creation capability.
        include_placeholder (bool): Flag to determine whether to include the image placeholder in the output.
        __name__ (str): Name of the provider.
        url (str): URL of the provider.
        working (bool): Indicates if the provider is operational.
        supports_stream (bool): Indicates if the provider supports streaming.
    """

    def __init__(
        self,
        provider: ProviderType,
        create_images: callable,
        create_async: callable,
        system_message: str = system_message,
        include_placeholder: bool = True
    ) -> None:
        """
        Initializes the CreateImagesProvider.

        Args:
            provider (ProviderType): The underlying provider.
            create_images (callable): Function to create images synchronously.
            create_async (callable): Function to create images asynchronously.
            system_message (str, optional): System message to be prefixed to messages. Defaults to a predefined message.
            include_placeholder (bool, optional): Whether to include image placeholders in the output. Defaults to True.
        """
        # The underlying provider to handle non-image related tasks.
        self.provider = provider
        # Function to create images synchronously.
        self.create_images = create_images
        # Function to create images asynchronously.
        self.create_images_async = create_async
        # System message to be prefixed to messages.
        self.system_message = system_message
        # Flag to determine whether to include the image placeholder in the output.
        self.include_placeholder = include_placeholder
        # Name of the provider.
        self.__name__ = provider.__name__
        # URL of the provider.
        self.url = provider.url
        # Indicates if the provider is operational.
        self.working = provider.working
        # Indicates if the provider supports streaming.
        self.supports_stream = provider.supports_stream

    def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        **kwargs
    ) -> CreateResult:
        """
        Creates a completion result, processing any image creation prompts found within the messages.

        Args:
            model (str): The model to use for creation.
            messages (Messages): The messages to process, which may contain image prompts.
            stream (bool, optional): Indicates whether to stream the results. Defaults to False.
            **kwargs: Additional keywordarguments for the provider.

        Yields:
            CreateResult: Yields chunks of the processed messages, including image data if applicable.

        Note:
            This method processes messages to detect image creation prompts. When such a prompt is found,
            it calls the synchronous image creation function and includes the resulting image in the output.
        """
        # Prefix the messages with the system message.
        messages.insert(0, {"role": "system", "content": self.system_message})
        buffer = ""
        # Iterate over chunks of the response from the provider.
        for chunk in self.provider.create_completion(model, messages, stream, **kwargs):
            # If the buffer is not empty or the chunk contains an image prompt.
            if buffer or "<" in chunk:
                buffer += chunk
                # If the buffer contains an image prompt.
                if ">" in buffer:
                    # Find the image prompt in the buffer.
                    match = re.search(r'<img data-prompt="(.*?)">', buffer)
                    # If an image prompt is found.
                    if match:
                        # Extract the placeholder and prompt from the match.
                        placeholder, prompt = match.group(0), match.group(1)
                        # Split the buffer into two parts: before and after the placeholder.
                        start, append = buffer.split(placeholder, 1)
                        # Yield the first part of the buffer.
                        if start:
                            yield start
                        # If the placeholder should be included in the output.
                        if self.include_placeholder:
                            # Yield the placeholder.
                            yield placeholder
                        # Log the image creation prompt.
                        if debug.logging:
                            print(f"Create images with prompt: {prompt}")
                        # Call the synchronous image creation function.
                        yield from self.create_images(prompt)
                        # Yield the second part of the buffer.
                        if append:
                            yield append
                    # If the buffer does not contain an image prompt, yield it.
                    else:
                        yield buffer
                    # Clear the buffer.
                    buffer = ""
            # If the chunk does not contain an image prompt, yield it.
            else:
                yield chunk

    async def create_async(
        self,
        model: str,
        messages: Messages,
        **kwargs
    ) -> str:
        """
        Asynchronously creates a response, processing any image creation prompts found within the messages.

        Args:
            model (str
