from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

async def speech_to_text(
    audio_path: str
):

    with open(
        audio_path,
        "rb"
    ) as audio_file:

        transcription = (
            client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3"
            )
        )

    return transcription.text