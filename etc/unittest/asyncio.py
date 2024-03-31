from .include import DEFAULT_MESSAGES  # Importing the default messages for chat completion
import asyncio                          # Importing the asyncio library for asynchronous programming

try:
    import nest_asyncio                 # Trying to import nest_asyncio library
    has_nest_asyncio = True             # Setting a flag to indicate if nest_asyncio is available
except:
    has_nest_asyncio = False            # Setting a flag to indicate if nest_asyncio is not available

import unittest                         # Importing the unittest library for testing
import g4f                              # Importing the g4f library
from g4f import ChatCompletion          # Importing the ChatCompletion class from g4f library
from .mocks import ProviderMock, AsyncProviderMock, AsyncGeneratorProviderMock  # Importing various mock classes for testing

class TestChatCompletion(unittest.TestCase):
    
    async def run_exception(self):
        """
        A coroutine that runs the ChatCompletion.create method with AsyncProviderMock and raises a NestAsyncioError.
        """
        return ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
        
    def test_exception(self):
        """
        Testing if a NestAsyncioError is raised when running the run_exception coroutine.
        """
        self.assertRaises(g4f.errors.NestAsyncioError, asyncio.run, self.run_exception())

    def test_create(self):
        """
        Testing the ChatCompletion.create method with default model and DEFAULT_MESSAGES using ProviderMock.
        """
        result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
        self.assertEqual("Mock", result)

    def test_create_generator(self):
        """
        Testing the ChatCompletion.create method with default model and DEFAULT_MESSAGES using AsyncGeneratorProviderMock.
        """
        result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
        self.assertEqual("Mock", result)

class TestChatCompletionAsync(unittest.IsolatedAsyncioTestCase):
    
    async def test_base(self):
        """
        Testing the ChatCompletion.create_async method with default model and DEFAULT_MESSAGES using ProviderMock.
        """
        result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
        self.assertEqual("Mock", result)

    async def test_async(self):
        """
        Testing the ChatCompletion.create_async method with default model and DEFAULT_MESSAGES using AsyncProviderMock.
        """
        result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)
        self.assertEqual("Mock", result)

    async def test_create_generator(self):
        """
        Testing the ChatCompletion.create_async method with default model and DEFAULT_MESSAGES using AsyncGeneratorProviderMock.
        """
        result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
        self.assertEqual("Mock", result)

class TestChatCompletionNestAsync(unittest.IsolatedAsyncioTestCase):
        
    def setUp(self) -> None:
        """
        Setting up the test environment by applying nest_asyncio if it is available.
        """
        if not has_nest_asyncio:
            self.skipTest('"nest_asyncio" not installed')
        nest_asyncio.apply()
        
    async def test_create(self):
        """
        Testing the ChatCompletion.create_async method with default model and DEFAULT_MESSAGES using ProviderMock.
        """
        result = await ChatCompletion.create_async(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
        self.assertEqual("Mock", result)

    async def test_nested(self):
       
