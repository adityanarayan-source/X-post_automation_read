"""
Response schemas for X posts (tweets).
"""

from typing import List, Optional

from pydantic import BaseModel


class Post(BaseModel):
    id: str
    text: str
    created_at: Optional[str] = None

class PostsResponse(BaseModel):
    success: bool
    data: List[Post]

class CreatePostRequest(BaseModel):
    text: str

class CreatePostResponse(BaseModel):
    success: bool
    data: Post