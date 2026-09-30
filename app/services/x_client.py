"""
Thin wrapper around the official X Python SDK (`xdk`).

All direct interaction with the X API SDK lives here. No other module
should import `xdk` directly. This keeps the SDK usage in one place so
future write operations (create_post, delete_post, etc.) can be added
without touching the API layer.
"""

from xdk import Client

from app.core.config import settings
from app.core.exceptions import XApiError


class XService:
    """Wraps the official xdk.Client for X API operations."""

    def __init__(self) -> None:
        access_token = settings.x_access_token.get_secret_value()
        if not access_token:
            # Fail fast at startup-adjacent time rather than on every request.
            raise XApiError(
                "X_ACCESS_TOKEN is not configured.", status_code=500
            )
        # OAuth 2.0 User Context: per the X SDK docs, an OAuth2 user
        # access token is passed directly as the bearer token.
        self._client = Client(access_token=access_token)

    def get_me(self) -> dict:
        """Fetch the currently authenticated X user via the SDK."""
        try:
            response = self._client.users.get_me(
                user_fields=["profile_image_url"]
            )
        except Exception as exc:  # xdk raises SDK-specific errors on failure
            # Never include the access token in the error message.
            raise XApiError(f"X API request failed: {exc}") from exc

        user = getattr(response, "data", None)
        if user is None:
            raise XApiError("X API returned no user data.")

        return {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "profile_image_url": getattr(user, "profile_image_url", None),
        }
    
    def create_post(self, text: str) -> dict:
        """Create a new post (tweet) via the SDK."""
        try:
            response = self._client.tweets.create_tweet(text=text)
        except Exception as exc:
            raise XApiError(f"X API request failed: {exc}") from exc

        post = getattr(response, "data", None)
        if post is None:
            raise XApiError("X API returned no post data.")

        return {
            "id": post.id,
            "text": post.text,
            "created_at": getattr(post, "created_at", None),
        }
        

    # Future write operations (e.g. create_post) go here, using the
    # same self._client instance.
    def get_my_posts(self, max_results: int = 10) -> list[dict]:
            """Fetch the authenticated user's most recent posts (tweets)."""
            me = self.get_me()
            try:
                pages = self._client.users.get_posts(
                    id=me["id"],
                    post_fields=["created_at"],
                    max_results=max_results,
                )
                first_page = next(iter(pages))
            except StopIteration:
                return []
            except Exception as exc:
                raise XApiError(f"X API request failed: {exc}") from exc
    
            posts = getattr(first_page, "data", None) or []
            return [
                {
                    "id": post.id,
                    "text": post.text,
                    "created_at": getattr(post, "created_at", None),
                }
                for post in posts
            ]


# Lazily constructed on first use so importing this module never touches
# the network or reads secrets prematurely.
_x_service: XService | None = None


def get_x_service() -> XService:
    global _x_service
    if _x_service is None:
        _x_service = XService()
    return _x_service