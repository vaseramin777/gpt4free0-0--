# Import necessary modules and functions
from g4f.Provider import __all__, ProviderUtils
from g4f import ChatCompletion
import concurrent.futures

# Define a list of provider names that should not be tested
_ = [
    'BaseProvider',
    'AsyncProvider',
    'AsyncGeneratorProvider',

