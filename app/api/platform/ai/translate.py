from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies.api_key import require_api_key
from app.engine.client import engine
from app.models.api_key import APIKey
from app.schemas.platform.error import ErrorResponse
from app.schemas.platform.translate import (
    TranslateRequest,
    TranslateResponse,
)

router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="Translate Text",
    description="""
Translate text between supported languages using Nativeee Engine.

Returns:

- Original text
- Translated text
- Generated audio URL (if available)
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
    api_key: APIKey = Depends(require_api_key),
):
    """
    Translate text using Nativeee Engine.
    """

    result = await engine.translate(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
    )

    return TranslateResponse(
        success=True,
        original=result["original"],
        translated=result["translated"],
        audio_url=result.get("audio_url"),
    )