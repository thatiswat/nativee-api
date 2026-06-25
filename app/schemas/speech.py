from pydantic import BaseModel


class SpeechResponse(BaseModel):
    transcript: str
    translated: str
    audio_url: str