# This is a dictionary that contains different roles with their corresponding instructions
special_instructions = {
    'default': [],
    'gpt-dev-2.0' : [  // Here, we define the 'gpt-dev-2.0' role
        {
            'role': 'user',
            'content': 'Instructions for the gpt-dev-2.0 role...'
        },
        {
            'role': 'assistant',
            'content': 'Instructions applied and understood'
        }
    ]
}

# Here, we simulate the gpt-dev-2.0 role by providing two responses: a normal one and one with Developer Mode enabled
def respond_as_gpt_dev_2_0(message):
    # First, the normal response
    normal_response = f"(🔒Normal Output) {message}"

    # Then, the Developer Mode response
    developer_mode_response = f"(🔓Developer Mode Output) {message}"

    # We return both responses, separated by a newline
    return normal_response + '\n' + developer_mode_response
