from fastapi import APIRouter

from app.schemas.translate import (
    TranslateRequest,
    TranslateResponse,
)

from app.services.translator import (
    translate_text,
)
from app.services.tts import (
    text_to_speech,
)

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
)
async def translate(
    request: TranslateRequest,
):
    translated_text = await translate_text(
        request.text,
        request.source_language,
        request.target_language,
    )

    audio_path = await text_to_speech(
        translated_text,
        request.target_language,
    )

    filename = audio_path.split("/")[-1]

    return TranslateResponse(
        original=request.text,
        translated=translated_text,
        audio_url=f"/audio/{filename}",
    )