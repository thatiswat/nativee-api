from fastapi import Request

from app.core.request_context import RequestContext
from app.models.api_key import APIKey


class RequestContextBuilder:
    """
    Builds a RequestContext for the current request.
    """

    def build(
        self,
        request: Request,
        api_key: APIKey,
    ) -> RequestContext:

        return RequestContext(
            request_id=request.headers.get(
                "X-Request-ID",
                "",
            ),
            api_key_id=api_key.id,
        )