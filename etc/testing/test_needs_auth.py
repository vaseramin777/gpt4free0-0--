import sys
from pathlib import Path # Import Path from pathlib to get the parent directory of the current file

import asyncio # Import asyncio for asynchronous tasks

# Import required functions from the testing.log_time module
from testing.log_time import log_time, log_time_async, log_time_yield

# Import the g4f module and its required components
import g4f
from g4f import Provider, ChatCompletion
from g4f.models import default # Use the default model for the ChatCompletion

# Define a list of providers to use for the chat completions
_providers = [
    Provider.H2o,
    Provider.You,
    Provider.HuggingChat,
    Provider.OpenAssistant,
    Provider.Bing,
    Provider.Bard
]

# Define the instruction to send to the chat completion providers
_instruct = "Hello, are you GPT 4?"

# Define a formatted example output for the chat completions
_example = """
<...>  <-- The output truncated for brevity
"""

# Print the Bing chat completion with streaming output
print("Bing: ", end="")
for response in log_time_yield(
    # Use the g4f.ChatCompletion.create function to get the chat completion
    # Set the provider to Bing, enable streaming output, and provide the instruction
    g4f.ChatCompletion.create,
    model=default,
    messages=[{"role": "user", "content": _instruct}],
    provider=Provider.Bing,
    stream=True,
    auth=True
):
    # Print the response as it arrives, flushing the output buffer after each print
    print(response, end="", flush=True)
print()
print()


# Define an asynchronous function to get the chat completions from all providers
async def run_async():
    # Create a list of coroutines, one for each provider
    responses = [
        log_time_async(
            # Use the provider's create_async method to get the chat completion asynchronously
            provider.create_async, 
            model=None,
            messages=[{"role": "user", "content": _instruct}],
        )
        for provider in _providers
    ]
    # Run all coroutines concurrently and wait for their completion
    responses = await asyncio.gather(*responses)
    # Print the chat completion for each provider
    for idx, provider in enumerate(_providers):
        print(f"{provider.__name__}:", responses[idx])
# Run the asynchronous function and measure the total time taken
print("Async Total:", asyncio.run(log_time_async(run_async)))
print()


# Define a function to get the chat completions from all providers with streaming output
def run_stream():
    # Iterate through the providers
    for provider in _providers:
        # Print the provider's name
        print(f"{provider.__name__}: ", end="")
        # Iterate through the chat completion messages with streaming output
        for response in log_time_yield(
            # Use the provider's create_completion method to get the chat completion
            # Set the provider, provide the instruction, and enable streaming output
            provider.create_completion,
            model=None,
            messages=[{"role": "user", "content": _instruct}],
        ):
            # Print the response as it arrives, flushing the output buffer after each print
            print(response, end="", flush=True)
        # Print a newline after all messages for the current provider have been processed
        print()
# Measure the total time taken for the run_stream function
print("Stream Total:", log_time(run_stream))
print()


# Define a function to get the chat completions from all providers without streaming output
def create_no_stream():
    # Iterate through the providers
    for provider in _providers:
        # Print the provider's name
        print(f"{provider.__name__}:", end=" ")
        # Iterate through the chat completion messages without streaming output
        for response in log_time_yield(
            # Use the provider's create_completion method to get the chat completion
            # Set the provider, provide the instruction, and disable streaming output
            provider
