# Import the tiktoken library to perform tokenization tasks
import tiktoken

# Import the Union type from the typing module to define a function return type
# that can be either an integer or a string
from typing import Union

# Define a function named 'tokenize' that accepts two arguments:
# 'text' (a required string argument) and 'model' (an optional string argument
# with a default value of 'gpt-3.5-turbo')
def tokenize(text: str, model: str = 'gpt-3.5-turbo') -> Union[int, str]:
    # Get the encoding for the specified model using the 'encoding_for_model'
    # function from the tiktoken library
    encoding = tiktoken.encoding_for_model(model)

    # Encode the input text using the encoding obtained from the model
    encoded = encoding.encode(text)
   
    # Calculate the number of tokens in the encoded text
    num_tokens = len(encoded)

    # Return the number of tokens and the encoded text as a tuple
    return num_tokens, encoded
