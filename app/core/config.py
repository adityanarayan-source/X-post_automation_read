"""
Application configuration.

Loads X API credentials and settings from environment variables (.env).
Sensitive values are stored as SecretStr so they are never accidentally
printed or logged in plain text.
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- X API OAuth 2.0 User Context credentials ---
    x_client_id: str = ""
    x_client_secret: SecretStr = SecretStr("")
    x_access_token: SecretStr = SecretStr("")
    x_refresh_token: SecretStr = SecretStr("")
    x_redirect_uri: str = ""
    x_scopes: str = "users.read,tweet.read,tweet.write"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "x_post_automation"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Single settings instance, imported wherever configuration is needed.
settings = Settings()
