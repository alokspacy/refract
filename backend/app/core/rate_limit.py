"""Rate limiting and retry-after header utilities."""
from fastapi import Response

def add_rate_limit_headers(response: Response, remaining: int, limit: int, retry_after_sec: int):
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
    if remaining <= 0:
        response.headers["Retry-After"] = str(retry_after_sec)
