# Import required modules
import codecs
import os
from setuptools import find_packages, setup

# Define the current working directory
here = os.path.abspath(os.path.dirname(__file__))

# Read the README.md file
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

# Set up the install requirements and extra requirements
INSTALL_REQUIRE = [
    "requests",
    "aiohttp",
]

EXTRA_REQUIRE = {
    # ... (extra requirements)
}

# Description of the package
DESCRIPTION = (
    'The official gpt4free repository | various collection of powerful language models'
)

# Set up the package using setuptools
setup(
    # Package details
    name='g4f',
    version=os.environ.get("G4F_VERSION"),
    author='Tekky',
    author_email='<support@g4f.ai>',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    package_data={
        'g4f': ['g4f/interference/*', 'g4f/gui/client/*', 'g4f/gui/server/*', 'g4f/Provider/npm/*']
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    entry_points={
        'console_scripts': ['g4f=g4f.cli:main'],
    },
    # Project URLs
    url='https://github.com/xtekky/gpt4free',  # Link to your GitHub repository
    project_urls={
        'Source Code': 'https://github.com/xtekky/gpt4free',  # GitHub link
        'Bug Tracker': 'https://github.com/xtekky/gpt4free/issues',  # Link to issue tracker
    },
    keywords=[
        # ... (keywords)
    ],
    classifiers=[
        # ... (classifiers)
    ],
)
