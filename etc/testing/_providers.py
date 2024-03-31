import sys
from pathlib import Path  # Importing Path from pathlib library to get the parent directory of the current file
from colorama import Fore, Style  # Importing Fore and Style from colorama library to add colors to the console output

# Adding the parent directory of the current file to the system path
sys.path.append(str(Path(__file__).parent.parent))

# Importing Provider, ProviderType, and models from g4f package
from g4f import Provider, ProviderType, models
from g4f.Provider import __providers__

def main():
    # Getting a list of providers
    providers = get_providers()
    failed_providers = []

    # Iterating over each provider
    for provider in providers:
        # Checking if the provider needs authentication
        if provider.needs_auth:
            continue
        # Printing the name of the provider
        print("Provider:", provider.__name__)
        # Calling the test function for the provider
        result = test(provider)
        # Printing the result of the test
        print("Result:", result)
        # Checking if the provider is working and the test result is False
        if provider.working and not result:
            # Adding the provider to the list of failed providers
            failed_providers.append(provider)
    # Printing a new line
    print()

    # Checking if there are any failed providers
    if failed_providers:
        # Printing the failed providers in red
        print(f"{Fore.RED + Style.BRIGHT}Failed providers:{Style.RESET_ALL}")
        for _provider in failed_providers:
            print(f"{Fore.RED}{_provider.__name__}")
    else:
        # Printing that all providers are working in green
        print(f"{Fore.GREEN + Style.BRIGHT}All providers are working")

# Getting a list of providers that are not deprecated or unfinished
def get_providers() -> list[ProviderType]:
    return [
        provider
        for provider in __providers__
        if provider.__name__ not in dir(Provider.deprecated)
        and provider.__name__ not in dir(Provider.unfinished)
    ]

# Creating a response for the provider
def create_response(provider: ProviderType) -> str:
    response = provider.create_completion(
        model=models.default.name,
        messages=[{"role": "user", "content": "Hello, who are you? Answer in detail much as possible."}],
        stream=False,
    )
    # Joining the response into a single string
    return "".join(response)

# Testing the provider
def test(provider: ProviderType) -> bool:
    try:
        # Creating a response for the provider

