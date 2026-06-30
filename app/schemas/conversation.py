from pydantic import BaseModel, ConfigDict


class ConversationMetrics(BaseModel):
    upload: float
    stt: float
    translation: float
    tts: float
    backend_total: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "upload": 0.18,
                "stt": 0.64,
                "translation": 0.09,
                "tts": 0.73,
                "backend_total": 1.81,
            }
        }
    )


class ConversationResult(BaseModel):
    success: bool
    request_id: str
    original: str
    translated: str
    audio_url: str
    metrics: ConversationMetrics

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "request_id": "req_01JZ4FQW4B3N2X7K8Y9Z",
                "original": "Hello, how are you?",
                "translated": "Hola, ¿cómo estás?",
                "audio_url": "/audio/9f6d8b3a.mp3",
                "metrics": {
                    "upload": 0.18,
                    "stt": 0.64,
                    "translation": 0.09,
                    "tts": 0.73,
                    "backend_total": 1.81,
                },
            }
        }
    )