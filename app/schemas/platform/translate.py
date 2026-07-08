from pydantic import BaseModel, ConfigDict


class TranslateRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


class TranslateResponse(BaseModel):
    success: bool
    original: str
    translated: str
    audio_url: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "original": "Hello, how are you?",
                "translated": "नमस्ते, आप कैसे हैं?",
                "audio_url": "/audio/8f3b6d2a.mp3",
            }
        }
    )