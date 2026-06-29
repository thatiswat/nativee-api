from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestContext:

    request_id: str

    api_key_id: Optional[int] = None

    endpoint: Optional[str] = None

    provider: Optional[str] = None

    latency_ms: float = 0

    success: bool = True
    