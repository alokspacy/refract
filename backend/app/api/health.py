import redis
from fastapi import APIRouter
from app.core.config import settings
from app.db.database import check_db_connection

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check endpoint")
def health_check():
    """Returns application health including PostgreSQL and Redis connection statuses."""
    db_ok = check_db_connection()

    redis_ok = False
    try:
        r = redis.from_url(settings.REDIS_URL, socket_connect_timeout=0.2, socket_timeout=0.2)
        redis_ok = r.ping()
    except Exception:
        redis_ok = False

    overall_status = "healthy" if db_ok else "degraded"

    return {
        "status": overall_status,
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "services": {
            "database": "connected" if db_ok else "disconnected",
            "redis": "connected" if redis_ok else "disconnected"
        }
    }
