from fastapi import APIRouter

from app.schemas.translate import (
    TranslateRequest,
    TranslateResponse,
)

from app.services.translator import translate_text
from app.services.tts import text_to_speech

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
)
async def translate(
    request: TranslateRequest,
):
    translated = await translate_text(
        request.text,
        request.source_language,
        request.target_language,
    )

    audio = await text_to_speech(
        translated,
        request.target_language,
    )

    filename = audio.split("/")[-1]

    return {
        "original": request.text,
        "translated": translated,
        "audio_url": f"/audio/{filename}",
    }