"""
Minimal MongoDB connectivity for storing generated posts.
"""

from datetime import datetime, timezone

from pymongo import MongoClient

from app.core.config import settings

_client: MongoClient | None = None


def _get_collection():
    global _client
    if _client is None:
        _client = MongoClient(settings.mongodb_uri)
    return _client[settings.mongodb_db_name]["posts"]


def save_post(post: dict) -> None:
    """Store a created post. Best-effort: a DB failure won't fail the request."""
    try:
        _get_collection().insert_one(
            {
                "x_post_id": post["id"],
                "text": post["text"],
                "created_at": datetime.now(timezone.utc),
            }
        )
    except Exception as exc:
        print(f"[warn] failed to save post to MongoDB: {exc}")