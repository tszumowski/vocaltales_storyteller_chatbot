import config
import gradio as gr
import openai
import os
import requests
import subprocess
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


# Main functions
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

    # call subprocess in background
    subprocess.Popen(["say", system_message["content"]])

    # Write current state of messages to file
    with open(config.TRANSCRIPT_PATH, "w") as f:
        for message in messages:
            f.write(f"{message['role']}: {message['content']}\n\n")

    return display_message


def generate_image(text_input: str) -> str:
    # Call OpenAI DALL-E using response
    prompt = text_input[: config.PROMPT_MAX_LEN]
    response = openai.Image.create(prompt=prompt, n=1, size=config.RESOLUTION)
    image_url = response["data"][0]["url"]
    img_data = requests.get(image_url).content
    with open(config.IMAGE_PATH, "wb") as handler:
        handler.write(img_data)
    return config.IMAGE_PATH


def clear_audio(audio):
    audio.value = None


# Gradio UI
with gr.Blocks() as ui:
    with gr.Row():
        with gr.Column(scale=1):
            # Audio Input Box
            audio_input = gr.Audio(source="microphone", type="filepath", label="Input")

            # # Button to clear the audio
            # clear_audio = gr.Button(label="Clear Audio")

            # User Input Box
            user_input = gr.Textbox(label="Transcription")

            # Story Output Box
            story_msg = gr.Textbox(label="Story")

        with gr.Column(scale=1):
            # Story Generated Image
            gen_image = gr.Image(label="Story Image", shape=(None, 5))

    # # Connect clear audio button to audio input
    # clear_audio.(clear_audio, audio_input)

    # Connect audio input to user input
    audio_input.change(transcribe_audio, audio_input, user_input)

    # Connect user input to story output
    user_input.change(chat_complete, user_input, story_msg)

    # Connect story output to image generation
    story_msg.change(generate_image, story_msg, gen_image)

ui.launch()
