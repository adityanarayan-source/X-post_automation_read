"""
Endpoints for the authenticated X user.
"""

from fastapi import APIRouter, HTTPException

from app.core.exceptions import XApiError
from app.schemas.user import MeResponse, XUser
from app.services.x_client import get_x_service

router = APIRouter()


@router.get("/api/v1/me", response_model=MeResponse)
def get_me() -> MeResponse:
    """Return the currently authenticated X user's basic profile info."""
    try:
        service = get_x_service()
        user_data = service.get_me()
    except XApiError as exc:
        # Log only a safe message; never log the access token.
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    return MeResponse(success=True, data=XUser(**user_data))
