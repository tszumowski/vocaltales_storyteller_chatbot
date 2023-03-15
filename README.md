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

Note there are two ways to speak the story: Mac or GCP Text-to-Speech. If using a Mac,
the Mac `say` command is used and that's the easiest/fastest route to running this.
It uses the System voice set up in the Accessibility settings.
However, if not on a Mac or if you prefer a more realistic voice, the GCP Text-to-Speech may be used.
This requires you having (a) a GCP project, (b) the TTS API enabled, and (c) your account authenticated
in gcloud (or GOOGLE_APPLICATION_CREDENTIALS environment variable set).

This application has only been tested on a Macbook.

1. Sign up at OpenAI and acquire an [OpenAI API key](https://platform.openai.com/account/api-keys).
1. Add to environment variable with: `export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxx`"
1. Create virtual environment
1. Run `pip install -r requirements.txt`
1. If on Mac, brew install `ffmpeg`: `brew install ffmpeg`

- Linux may need to install also but untested.

1. Review and update config in `config.py` as desired
1. If using GCP TTS
1. set in `config.py`: `SPEECH_METHOD = SpeechMethod.GCP`
1. Navigate to the [Google API page](https://console.cloud.google.com/apis/api/texttospeech.googleapis.com/) and enable the API
1. Confirm you are authenticated in gcloud and your account has access to that API.
1. Run with: `python storyteller.py`
1. Navigate to `http://127.0.0.1:7860/` and have fun!

## Running as Docker Container

Replace `<service-name>` with a name of your choice.

1. Build Docker image: `docker build -t <image-name> .`
1. Run locally with something similar to:

```
docker run -it --rm \
    -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/creds.json \
    -v ${HOME}/.config/gcloud/application_default_credentials.json:/tmp/creds.json \
    -e OPENAI_API_KEY=<openai-api-key> -p <port>:7860 audio-storyteller
```

Fill in: `<openai-api-key> and <port>. Then once up. Navigate on a browser to `127.0.0.1:<port>`

## Deploying to Google Cloud Run

1. Follow the directions above to create a local docker image.
1. Tag and push (Note: Follow [these directions](https://cloud.google.com/container-registry/docs/advanced-authentication) to authenticate)
   ```
   docker tag <image-name> gcr.io/<project-id>/<image-name>
   docker push gcr.io/<project-id>/<image-name>
   ```
1. Deploy: `gcloud run deploy <service-name> --image gcr.io/<project-id>/<image-name> --platform managed`

Cloud Run will automatically scale the number of instances based on the incoming traffic. You can access the deployed Gradio application via the URL provided by the Cloud Run service.
