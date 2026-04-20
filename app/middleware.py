from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    _allowed = re.compile(r"[^A-Za-z0-9._-]")

    @classmethod
    def _safe_correlation_id(cls, raw: str | None) -> str:
        if not raw:
            return f"req-{uuid.uuid4().hex[:8]}"
        cleaned = cls._allowed.sub("_", raw.strip())[:64]
        if not cleaned:
            return f"req-{uuid.uuid4().hex[:8]}"
        return cleaned

    async def dispatch(self, request: Request, call_next):
        clear_contextvars()

        correlation_id = self._safe_correlation_id(request.headers.get("x-request-id"))
        bind_contextvars(correlation_id=correlation_id)
        request.state.correlation_id = correlation_id

        start = time.perf_counter()
        response = await call_next(request)

        try:
            response.headers["x-request-id"] = correlation_id
        except Exception:
            pass

        try:
            response.headers["x-response-time-ms"] = str(int((time.perf_counter() - start) * 1000))
        except Exception:
            pass
        return response
