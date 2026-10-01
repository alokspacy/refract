"""Central API Router registry."""
from fastapi import APIRouter
from app.api import auth, documents, health, jobs, variants, profiles, compliance, readability, audio

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(variants.router)
api_router.include_router(profiles.router)
api_router.include_router(jobs.router)
api_router.include_router(compliance.router)
api_router.include_router(readability.router)
api_router.include_router(audio.router)
