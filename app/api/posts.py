"""
Endpoints for reading the authenticated user's posts (tweets).
"""

from fastapi import APIRouter, HTTPException, Query

from app.core.exceptions import XApiError
from app.schemas.post import Post, PostsResponse
from app.services.x_client import get_x_service
from app.schemas.post import CreatePostRequest, CreatePostResponse, Post, PostsResponse
from app.services.db import save_post

router = APIRouter()


@router.get("/api/v1/me/tweets", response_model=PostsResponse)
def get_my_tweets(max_results: int = Query(10, ge=5, le=100)) -> PostsResponse:
    """Return the currently authenticated user's most recent posts."""
    try:
        service = get_x_service()
        posts_data = service.get_my_posts(max_results=max_results)
    except XApiError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    return PostsResponse(success=True, data=[Post(**p) for p in posts_data])

@router.post("/api/v1/posts", response_model=CreatePostResponse)
def create_post(payload: CreatePostRequest) -> CreatePostResponse:
    try:
        service = get_x_service()
        result = service.create_post(payload.text)
    except XApiError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)

    save_post(result)
    return CreatePostResponse(success=True, data=Post(**result, created_at=None))