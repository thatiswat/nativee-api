from pydantic import BaseModel


class ConversationMetrics(BaseModel):
    upload: float
    stt: float
    translation: float
    tts: float
    backend_total: float


class ConversationResult(BaseModel):
    success: bool

    request_id: str

    original: str

    translated: str

    audio_url: str

    metrics: ConversationMetrics