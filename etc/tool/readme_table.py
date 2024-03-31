import re
import sys
from pathlib import Path  # Imported to work with file paths
from urllib.parse import urlparse  # Used to extract the netloc part of a URL

# Importing required modules from the g4f package
from g4f import models
from g4f import ChatCompletion
from g4f.Provider.base_provider import BaseProvider
from g4f import debug  # For logging purposes

# Importing a utility function from a local testing module
from etc.testing._providers import get_providers

# Setting debug.logging to True for enabling logging
debug.logging = True

# An async function to test a single provider
async def test_async(provider: type[BaseProvider]):
    if not provider.working:  # If the provider is not working
        return False  # Return False

    messages = [{"role": "user", "content": "Hello Assistant!"}]
    try:
        response = await asyncio.wait_for(ChatCompletion.create_async(
            model=models.default,  # Using the default model
            messages=messages,
            provider=provider
        ), 30)  # Waiting for the response for a maximum of 30 seconds
        return bool(response)  # Return True if the response is not empty, otherwise False
    except Exception as e:
        if debug.logging:
            print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
        return False  # Return False if any exception occurs


# An async function to test a list of providers
async def test_async_list(providers: list[type[BaseProvider]]):
    responses: list = [
        test_async(_provider)  # Testing each provider asynchronously
        for _provider in providers
    ]
    return await asyncio.gather(*responses)  # Gathering the results


# A function to print the provider information
def print_providers():

    providers = get_providers()  # Getting the list of providers
    responses = asyncio.run(test_async_list(providers))  # Testing the providers

    # Printing the table header
    for type in ("GPT-4", "GPT-3.5", "Other"):
        lines = [
            "",
            f"### {type}",
            "",
            "| Website | Provider | GPT-3.5 | GPT-4 | Stream | Status | Auth |",
            "| ------  | -------  | ------- | ----- | ------ | ------ | ---- |",
        ]

        # Printing the table rows for each provider
        for is_working in (True, False):
            for idx, _provider in enumerate(providers):
                if is_working != _provider.working:
                    continue
                do_continue = False
                if type == "GPT-4" and _provider.supports_gpt_4:
                    do_continue = True
                elif type == "GPT-3.5" and not _provider.supports_gpt_4 and _provider.supports_gpt_35_turbo:
                    do_continue = True
                elif type == "Other" and not _provider.supports_gpt_4 and not _provider.supports_gpt_35_turbo:
                    do_continue = True
                if not do_continue:
                    continue
                netloc = urlparse(_provider.url).netloc  # Extracting the netloc part of the URL
                website = f"[{netloc}]({_provider.url})"  # Creating the website link

                provider_name = f"`g4f.Provider.{_provider.__name__}`"  # Creating the provider name

                has_gpt_35 = "✔️" if _provider.supports_gpt_35_turbo else "❌"  # Checking if the provider supports GPT-3.5
                has_gpt_4 = "✔️" if _provider.supports_gpt_4 else "❌"  # Checking if the provider supports GPT-4
                stream = "✔️" if _provider.supports_stream else "❌"  # Checking if the provider supports streaming
                if _provider.working:
                    status = '![Active](https://img.shields.io/badge/Active-brightgreen)'  # Setting the status to active
                    if responses[idx]:
                        status = '![Active](https://img.shields.io/badge/Active-brightgreen)'  # If the provider passed the test, setting the status to active
                    else:
                        status = '![Unknown](https://img.shields.io/badge/Unknown-grey)'  # If the provider failed the test, setting the status to unknown
                else:
                    status = '![Inactive](https://img.shields.io/badge/Inactive-red)'  # Setting the status to inactive
                auth = "✔️" if _provider.needs_auth else "❌"  # Checking if the provider needs authentication

                lines.append(
                    f"| {website} | {provider_name} | {has_gpt_35} | {has_gpt_4} | {stream} | {status} | {auth} |"
                )
        print("\n".join(lines))  # Printing the table rows


# A function to print the model information
def print_models():
    base_provider_names = {
        "cohere": "Cohere",
        "google": "Google",
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "replicate": "Replicate",
        "huggingface": "Huggingface",
    }
    provider_urls = {
        "Bard": "https://bard.google.com/",
        "H2o": "https://www.h2o.ai/",
        "Vercel": "https://sdk.vercel.ai/",
    }

    lines = [
        "| Model | Base Provider | Provider | Website |",

