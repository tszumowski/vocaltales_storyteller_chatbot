import config
import gradio as gr
import openai
import os
import requests
import subprocess

from config import SpeechMethod
from google.cloud import texttospeech
from typing import BinaryIO


# Set OpenAI API Key
openai.api_key = os.environ.get("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OpenAI API Key not set as environnment variable OPENAI_API_KEY")

# Initial message
messages = [
    {
        "role": "system",
        "content": config.INITIAL_PROMPT,
    }
]


"""
Main functions
"""


def transcribe_audio(audio: BinaryIO) -> str:
    # Open audio file and transcribe
    with open(audio, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text_transcription = transcript["text"]

    return text_transcription


def chat_complete(text_input: str) -> str:
    global messages

    # Append to messages for chat completion
    messages.append({"role": "user", "content": text_input})

    # Fetch response from OpenAI
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    # Extract and store message
    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    # Return message to display
    display_message = system_message["content"]

    if config.SPEECH_METHOD == SpeechMethod.MAC:
        # call subprocess in background
        subprocess.Popen(["say", system_message["content"]])

    # Write current state of messages to file
    with open(config.TRANSCRIPT_PATH, "w") as f:
        for message in messages:
            f.write(f"{message['role']}: {message['content']}\n\n")

    return display_message


def generate_image(text_input: str) -> str:
    """
    Generate an image using DALL-E via OpenAI API.

    Args:
        text_input: Text to use as prompt for image generation

    Returns:
        str: Path to generated image
    """
    prompt = text_input[: config.PROMPT_MAX_LEN]
    response = openai.Image.create(prompt=prompt, n=1, size=config.RESOLUTION)
    image_url = response["data"][0]["url"]
    img_data = requests.get(image_url).content
    with open(config.IMAGE_PATH, "wb") as handler:
        handler.write(img_data)
    return config.IMAGE_PATH


# Call Google Cloud Text-to-Speech API to convert text to speech
def text_to_speech(input_text: str) -> str:
    """
    Use GCP Text-to-Speech API to convert text to a WAV file.

    Args:
        input_text: Text to convert to speech

    Returns
        str: Path to output audio file
    """
    print(f"Convert text to speech: {input_text}")
    # set up the client object
    client = texttospeech.TextToSpeechClient()

    # set up the synthesis input object
    synthesis_input = texttospeech.SynthesisInput(text=input_text)

    # set up the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code=config.TTS_VOICE_LANGUAGE_CODE, name=config.TTS_VOICE
    )

    # set up the audio parameters
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
    )

    # generate the request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # save the response audio as an MP3 file
    with open(config.GENERATED_SPEECH_PATH, "wb") as out:
        out.write(response.audio_content)

    # return response.audio_content
    return config.GENERATED_SPEECH_PATH


"""
Gradio UI Definition
"""
with gr.Blocks(analytics_enabled=False, title="Audio Storyteller") as ui:
    with gr.Row():
        with gr.Column(scale=1):
            # Audio Input Box
            audio_input = gr.Audio(
                source="microphone", type="filepath", label="User Audio Input"
            )

            # User Input Box
            transcribed_input = gr.Textbox(label="Transcription")

            # Story Output Box
            story_msg = gr.Textbox(label="Story")

            # Add components for TTS
            if config.SPEECH_METHOD == SpeechMethod.GCP:
                # Audio output box if using Google Cloud TTS
                audio_output = gr.Audio(label="Output", elem_id="speaker")

                # Just a sink to pass through and trigger Javascript audio autoplay on
                text_sink = gr.Textbox(label="Debug", visible=False)

        with gr.Column(scale=1):
            # Story Generated Image
            gen_image = gr.Image(label="Story Image", shape=(None, 5))

    # Connect audio input to user input
    audio_input.change(transcribe_audio, audio_input, transcribed_input)

    # Connect user trainput to story output
    transcribed_input.change(chat_complete, transcribed_input, story_msg)

    # Connect story output to image generation
    story_msg.change(generate_image, story_msg, gen_image)

    """
    Used for GCP TTS only

    Workaround: Custom (hacky) Javascript function to autoplay audio
    Derived from: https://github.com/gradio-app/gradio/issues/1349
    Needs a timeout to wait for the Google TTS call to complete and the audio
    file sent to the gradio object in browser.
    """
    autoplay_audio = """
            async () => {{
                setTimeout(() => {{
                    document.querySelector('#speaker audio').play();
                }}, {speech_delay});
            }}
        """.format(
        speech_delay=int(config.TTS_SPEECH_DELAY * 1000)
    )

    if config.SPEECH_METHOD == SpeechMethod.GCP:
        # Connect story output to audio output after calling TTS on it
        story_msg.change(text_to_speech, story_msg, audio_output)

        # Separately trigger the autoplay audio function
        story_msg.change(None, None, None, _js=autoplay_audio)

ui.launch()
