"""
FastAPI application entrypoint.

Only responsible for creating the app and registering routers.
No X SDK logic lives here.
"""

from fastapi import FastAPI

from app.api import health, users,posts

app = FastAPI(
    title="X-post_automation",
    version="0.1.0",
    description="Minimal FastAPI backend for the X API (read-only POC).",
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(posts.router)  

