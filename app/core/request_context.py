from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestContext:
    """
    Carries request metadata through the platform lifecycle.

    This context is populated by middleware and enriched by services,
    allowing usage logging, analytics, monitoring, and future billing
    without coupling business logic to platform concerns.
    """

    request_id: str

    api_key_id: Optional[int] = None
    plan_id: Optional[int] = None

    endpoint: Optional[str] = None
    method: Optional[str] = None

    provider: Optional[str] = None

    latency_ms: float = 0.0
    status_code: int = 200

    success: bool = True