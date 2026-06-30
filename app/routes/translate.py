from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies.auth import require_api_key
from app.providers.edge_provider import text_to_speech
from app.providers.registry import ProviderRegistry
from app.schemas.error import ErrorResponse
from app.schemas.translate import (
    TranslateRequest,
    TranslateResponse,
)

router = APIRouter(
    tags=["Translation"],
)


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="Translate Text",
    description="""
Translate text between supported languages.

Uses the configured translation provider through
the Provider Registry.

Returns:

- Original text
- Translated text
- Generated audio URL
""",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid translation request",
        },
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
        },
        403: {
            "model": ErrorResponse,
            "description": "API key disabled",
        },
        429: {
            "model": ErrorResponse,
            "description": "Rate limit or monthly quota exceeded",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
async def translate_endpoint(
    request: TranslateRequest,
    api_key: str = Depends(require_api_key),
):
    """
    Translate text into another language and generate
    speech for the translated result.
    """

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
        success=True,
        original=request.text,
        translated=translated_text,
        audio_url=f"/audio/{filename}",
    )