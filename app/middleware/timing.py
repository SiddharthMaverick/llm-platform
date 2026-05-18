import time

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from app.core.logging import logger


class TimingMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        start_time = time.time()

        response = await call_next(request)

        process_time = (
            time.time() - start_time
        )

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"completed in "
            f"{process_time:.2f}s"
        )

        return response