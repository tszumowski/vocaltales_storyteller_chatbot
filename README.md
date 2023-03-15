# Children's Storytelling Audio Chatbot

---

This is a Gradio UI application that takes in a request for a story from the microphone
and speaks an interactive Choose-Your-Own-Adventure style children's story. It leverages:

- [OpenAI Whisper](https://openai.com/research/whisper): to transcribe user audio input request
- [OpenAI ChatGPT (3.5-turbo)](https://platform.openai.com/docs/models/gpt-3-5):
  to generate a story chapter given the user's inputs
- (Optional) [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/):
  to use realistic voices when telling the story.

## Pricing

**WARNING: This application uses paid API services. Create quotas and watch your usage.**

At the time of writing, the pricing is as follows:

- [whisper](https://openai.com/pricing): $0.006 / minute (rounded to the nearest second)
- [gpt-3.5-turbo](https://openai.com/pricing): $0.002 / 1K tokens
- [Google Text-to-Speech](https://cloud.google.com/text-to-speech/pricing):
  - 0 to 1 million bytes free per month
  - $0.000016 USD per byte ($16.00 USD per 1 million bytes)

Check the links as these can change often. But at the time of writing it costs less
than one USD for light use.

Both OpenAI and Google offer free credits for new users.

## Setup

TODO: Describe mac vs. GCP

This application has only been tested on a Macbook.

1. Sign up at OpenAI and acquire an [OpenAI API key](https://platform.openai.com/account/api-keys).
1. Add to environment variable with: `export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxx`"
1. Create virtual environment
1. Run `pip install -r requirements.txt`
1. If on Mac, brew install `ffmpeg`: `brew install ffmpeg`
  * Linux may need to install also but untested.
1. Review and update config in `config.py` as desired
1. If using GCP TTS
  1. set in `config.py`: `SPEECH_METHOD = SpeechMethod.GCP`
  1. TODO: Mention
1. Run with: `python storyteller.py`
1. Navigate to `http://127.0.0.1:7860/` and have fun!

## TODO

- [ ] Document
- [ ] Add directions for getting TTS key
- [ ] Report updated code after committed to github issue referenced in gradio
