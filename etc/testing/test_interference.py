# type: ignore
# This line is used to ignore any type checking errors that might occur during the execution of this script.

import openai
# The openai module is imported for using the OpenAI API to generate a poem about a tree.

openai.api_key = ""
# The API key for OpenAI is set here. It should be replaced with a valid key to use the API.

openai.api_base = "http://localhost:1337"
# The base URL for the OpenAI API is set here. In this case, it is set to a local server running on port 1337.


def main():
    # The main function is defined here. It contains the code to generate a poem about a tree using the OpenAI API.

    chat_completion = openai.ChatCompletion.create(
        # The ChatCompletion.create() method from the openai module is called to start a new chat completion session.

        model="gpt-3.5-turbo",
        # The model to be used for the chat completion is set to "gpt-3.5-turbo".

        messages=[{"role": "user", "content": "write a poem about a tree"}],
        # The prompt for the chat completion is set to "write a poem about a tree".

        stream=True,
        # The stream parameter is set to True to receive the chat completion response in a streamed manner.
    )

    if isinstance(chat_completion, dict):
        # The type of the chat_completion variable is checked here.

        # If chat_completion is a dictionary, it means that the response was not streamed.

        print(chat_completion.choices[0].message.content)
        # The content of the first choice in the chat completion response is printed.

    else:
        # If chat_completion is not a dictionary, it means that the response was streamed.

        for token in chat_completion:
            # The streamed response is iterated over, token by token.

            content = token["choices"][0]["delta"].get("content")
