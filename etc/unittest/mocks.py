# Import the necessary classes from the 'g4f.Provider.base_provider' module
from g4f.Provider.base_provider import AbstractProvider, AsyncProvider, AsyncGeneratorProvider

# Define a new class 'ProviderMock' that inherits from the 'AbstractProvider' class
class ProviderMock(AbstractProvider):
    # Initialize the 'working' attribute to True
    working = True

    # Define the 'create_completion' method that takes in 'model', 'messages', 'stream', and keyword arguments 'kwargs'
    def create_completion(
        # Specify the 'model' parameter
        model,
        # Specify the 'messages' parameter
        messages,
        # Specify the 'stream' parameter
        stream,
        **kwargs
    ):
        # Yield the string 'Mock'
        yield "Mock"
        
# Define a new class 'AsyncProviderMock' that inherits from the 'AsyncProvider' class
class AsyncProviderMock(AsyncProvider):
    # Initialize the 'working' attribute to True
    working = True

    # Define the 'create_async' method that takes in 'model', 'messages', and keyword arguments 'kwargs'
    async def create_async(
        # Specify the 'model' parameter
        model,
        # Specify the 'messages' parameter
        messages,
        **kwargs
    ):
        # Return the string 'Mock'
        return "Mock"

# Define a new class 'AsyncGeneratorProviderMock' that inherits from the 'AsyncGeneratorProvider' class
class AsyncGeneratorProviderMock(AsyncGeneratorProvider):
    # Initialize the 'working' attribute to True
    working = True

    # Define the 'create_async_generator' method that takes in 'model', 'messages', 'stream', and keyword arguments 'kwargs'
    async def create_async_generator(
        # Specify the 'model' parameter
        model,
        # Specify the 'messages' parameter
        messages,
        # Specify the 'stream' parameter
        stream,
        **kwargs
    ):
        # Yield the string 'Mock'
        yield "Mock"
        
# Define a new class 'ModelProviderMock' that
