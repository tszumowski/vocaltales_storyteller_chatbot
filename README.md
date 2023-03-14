# Children's Storytelling Audio Chatbot

---

TODO: Document. Medium?
Make note of pricing.

## Setup

1. Get an OpenAI API key.
1. Add to environment variable with: `export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxx`"
1. Create virtual environment
1. `pip install -r requirements.txt`
1. Brew install `ffmpeg`: `brew install ffmpeg`
1. Update config in `config.py` as desired
1. Run with: `python storyteller.py`
1. Navigate to `http://127.0.0.1:7860/` and have fun!

## TODO

- [ ] Fix the audio thread error that pops up
- [ ] Document

- [ ] Add directions for getting TTS key
- [ ] Add option to use local system or Google TTS (or if key not provided)
- [ ] Try using audio change from demo since doesn't seem to work (change or upload event)
- [ ] Report updated code after committed to github issue referenced in gradio
