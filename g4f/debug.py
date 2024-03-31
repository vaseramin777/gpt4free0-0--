from .base_provider import ProviderType  # Importing the ProviderType class from the base_provider module.

logging: bool = False  # Setting a flag to control whether logging is enabled or not (default is False).
version_check: bool = True  # Setting a flag to control whether to perform a version check (default is True).
last_provider: ProviderType = None  # Initializing a variable to store the last provider used (default is None).
