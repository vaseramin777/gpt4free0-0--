import unittest
import asyncio
import g4f
from g4f import ChatCompletion, get_last_provider
from g4f.Provider import RetryProvider
from .mocks import ProviderMock

# The DEFAULT_MESSAGES variable is a list of dictionaries that define the default messages used in the ChatCompletion.create method.
DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class NoTestChatCompletion(unittest.TestCase):

    # The no_test_create_default method tests the ChatCompletion.create method with the default model and messages.
    # It asserts that the result contains the string "Hello".
    def no_test_create_default(self):
        result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES)
        if "Good" not in result and "Hi" not in result:
            self.assertIn("Hello", result)

    # The no_test_bing_provider method tests the ChatCompletion.create method with the Bing provider and default messages.
    # It asserts that the result contains the string "Bing".
    def no_test_bing_provider(self):
        provider = g4f.Provider.Bing
        result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, provider)
        self.assertIn("Bing", result)

class TestGetLastProvider(unittest.TestCase):

    # The test_get_last_provider method tests the get_last_provider function after calling ChatCompletion.create with the ProviderMock.
    # It asserts that the last provider is equal to ProviderMock.
    def test_get_last_provider(self):
        ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
        self.assertEqual(get_last_provider(), ProviderMock)

    # The test_get_last_provider_retry method tests the get_last_provider function after calling ChatCompletion.create with the RetryProvider and ProviderMock.
    # It asserts that the last provider is equal to ProviderMock.
    def test_get_last_provider_retry(self):
        ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, Ret
