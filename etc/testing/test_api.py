import openai  # Import the OpenAI library to interact with the API

# Set your Hugging Face token as the API key if you use embeddings
# If you don't use embeddings, leave it empty
openai.api_key = "YOUR_HUGGING_FACE_TOKEN"  # Replace with your actual token

# Set the API base URL if needed, e.g., for a local development environment
openai.api_base = "http://localhost:1337/v1"

def main():
    # Call the ChatCompletion.create method from the OpenAI library
    # to generate a poem about a tree
    response = openai.ChatCompletion.create(
        # Select the gpt-3.5-turbo model for the generation
        model="gpt-3.5-turbo",
        # Provide the user message to generate a poem about a tree
        messages=[{"role": "user", "content": "write a poem about a tree"}],
        # Enable streaming of the generated content
        stream=True,
    )
    
    # Check if the response is not a stream
    if isinstance(response, dict):
        # Print the generated poem content
        print(response.choices[0].message.content)
    else:
        # Streaming is enabled
        for token in response:
            # Get the content of the generated token
            content = token["choices"][0]["delta"].get("content")
            # Print the content without adding a newline
            if content is not None:
                print(content, end="", flush=True)

if __name__ == "__main__":
    # Call the main function when the script is run directly
    main()
