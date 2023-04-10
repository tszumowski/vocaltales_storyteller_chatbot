from enum import Enum

"""
Speech method
    None: No speech
    "gcp": Google Cloud Platform Text-to-Speech API
    "mac": Mac OS X say command
    "elevenio": Eleven.io Text-to-Speech API

Note: For GCP, you must be authenticated with the gcloud CLI or set the
GOOGLE_APPLICATION_CREDENTIALS environment variable

For Eleven.io you need to add an ELEVENIO_API_KEY as environment variable with key
"""


# Define the class enum
class SpeechMethod(Enum):
    NONE = 1
    GCP = 2
    MAC = 3
    ELEVENIO = 4


# Set the method here
SPEECH_METHOD = SpeechMethod.GCP


"""
Other configuration
"""
RESOLUTION = "512x512"  # One of 256x256, 512x512, 1024x1024
PROMPT_MAX_LEN = 1000  # Max length of prompt for DALL-E
IMAGE_PATH = "generated_image.jpg"  # path to save generated image
GENERATED_SPEECH_PATH = "generated_speech.mp3"
TTS_SPEECH_DELAY = 5.0  # seconds to wait before playing generated speech

"""
Voice for GCP Text-to-Speech API
Samples & More Options at: https://cloud.google.com/text-to-speech/docs/voices
Keys are derived from the Google naming scheme in the above site.
"""
TTS_VOICE_DEFAULT = "US Female"
TTS_VOICE_OPTIONS = {
    "AU Female": "en-AU-Neural2-C",
    "AU Male": "en-AU-Neural2-B",
    "US Female": "en-US-Neural2-C",
    "US Male": "en-US-Neural2-D",
    "GB Female": "en-GB-Neural2-C",
    "GB Male": "en-GB-Neural2-D",
}

"""
Eleven.io Text-to-Speech API Config
"""
# can get the ID of voice through API /voice URL or look at the URL called when
# generating online
"""
curl --location 'https://api.elevenlabs.io/v1/voices' \
--header 'xi-api-key: [API_KEY]' \
--header 'Accept: application/json'
"""
# TODO: Can make options like GCP above to make this more generic
ELEVENIO_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
ELEVENIO_TTS_BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"

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

"""
INSTRUCTIONS
"""
INSTRUCTIONS_TEXT = """
            Instructions:

            VocalTales is a audio-based storytelling chatbot. It will generate a story
            chapter from your input and ask you what to do next. After each entry,
            it will speak the story in the selected voice and generate an image based
            on the current story contents.

            1. Select the voice type in this box.
            1. Press `Record from microphone.
            1. Speak your story input.
            1. Wait for the story to be generated and image to be generated.
            1. If audio doesn't start automatically, Press the `Play` button in
            the `Output` box.
            1. When ready to provide another input, under `User Audio Input`, press the
            `X` in the top-right corner to clear the last recording. Then press
            `Record from microphone` again and speak your next input.

            Note: When you press `X` you may see a red `Error` in a box. That is normal.


            References:
            - Source Code: https://github.com/tszumowski/vocaltales_storyteller_chatbot
            - [Medium Article](https://medium.com/@tszumowski/f796fc715dcb)
            """  # NOQA
