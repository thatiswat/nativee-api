from fastapi import (
    APIRouter,
    Depends,
)

from app.core.security import require_api_key

from app.schemas.translate import (
    TranslateRequest,
    TranslateResponse,
)

from app.providers.registry import (
    ProviderRegistry,
)
from app.providers.edge_provider import text_to_speech

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
)
async def translate_endpoint(
    request: TranslateRequest,
    api_key: str = Depends(require_api_key),
):
    translated_text = await ProviderRegistry.translate(
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