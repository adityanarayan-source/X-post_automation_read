"""
Response schemas for the authenticated X user.
"""

from typing import Optional

from pydantic import BaseModel


class XUser(BaseModel):
    id: str
    name: str
    username: str
    profile_image_url: Optional[str] = None


class MeResponse(BaseModel):
    success: bool
    data: XUser
