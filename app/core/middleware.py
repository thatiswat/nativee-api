import secrets
import time

from fastapi import Request

from app.core.logger import logger


async def benchmark(
    request: Request,
    call_next,
):

    request.state.id = secrets.token_hex(4)

    start = time.perf_counter()

    response = await call_next(
        request,
    )

    elapsed_ms = (
        time.perf_counter()
        - start
    ) * 1000

    response.headers["X-Request-Time"] = (
        f"{elapsed_ms:.2f}ms"
    )

    response.headers["X-Request-ID"] = (
        request.state.id
    )

    logger.info(
        "[%s] %s %s %.2fms",
        request.state.id,
        request.method,
        request.url.path,
        elapsed_ms,
    )

    return response