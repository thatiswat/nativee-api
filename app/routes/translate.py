from fastapi import APIRouter

from app.schemas.translate import (
    TranslateRequest,
    TranslateResponse,
)

from app.router.translation_router import translate
from app.providers.edge_provider import text_to_speech

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
)
async def translate_endpoint(
    request: TranslateRequest,
):
    translated_text = await translate(
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