import unittest
import g4f
from g4f import ChatCompletion
from .mocks import ModelProviderMock # Importing the mock provider for testing

# Define the default messages to be used in the tests
DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

# Create a test model with a specific name and provider
test_model = g4f.models.Model(
    name="test/test_model",  # Name of the model
    base_provider="",  # Base provider for the model
    best_provider=ModelProviderMock  # Mock provider for testing
)

# Register the test model with ModelUtils for conversion
g4f.models.ModelUtils.convert["test_model"] = test_model

# Test case class for testing the model
class TestPassModel(unittest.TestCase):

    # Test to check if the model instance is created correctly
    def test_model_instance(self):
        response = ChatCompletion.create(test_model, DEFAULT_MESSAGES)
        self.assertEqual(test_model.name, response)

    # Test to check if the model name is passed correctly
    def test_model_name(self):
        response = ChatCompletion.create("test_model", DEFAULT_MESSAGES)
        self.assertEqual(test_model.name, response)

    # Test to check if the model is passed correctly with the mock provider
    def test_model_pass(self):
        response = ChatCompletion.create("test/test_model", DEFAULT_MESSAGES, ModelProviderMock)
        self.assertEqual(test_model.name, response)
