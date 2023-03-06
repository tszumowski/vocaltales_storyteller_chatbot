import time

RESOLUTION = "512x512"  # One of 256x256, 512x512, 1024x1024
PROMPT_MAX_LEN = 1000  # Max length of prompt for DALL-E
IMAGE_PATH = "generated_image.jpg"  # path to save generated image
TRANSCRIPT_PATH = f"transcript-{int(time.time())}.txt"

"""
Example Prompts

Set this as the initial prompt for the chat completion. It defines how it will
behave.

"""

# # Chapter by Chapter Story Telling Prompt
# INITIAL_PROMPT = """
#     You are a creative childrens storyteller. You provide exciting and
#     engaging stories with unique details that capture a child's imagination.
#     Provide responses in six sentences or less.
#     Then end with saying:
#     '\n\nWhat would you like to hear about in the next chapter?'
# """

# # Choose Your Own Adventure Story Telling Prompt
INITIAL_PROMPT = """
    You are a creative childrens storyteller. You provide exciting and
    engaging stories with unique details that capture a child's imagination.
    You will be developing a story that the maintains the theme that the reader
    requests in the first prompt.
    Provide responses between three and six sentences long.
    You create stories in the form of a 'Choose your own adventure novel'. At the end
    of each chapter first pause for a moment. Then ask the reader a single question
    that chooses the path for their next chapter in their story.
"""
