import os
from groq import Groq


def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY is missing")

    return Groq(api_key=api_key)


async def speech_to_text(audio_path: str):

    client = get_client()

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3"
        )

    return transcription.text
