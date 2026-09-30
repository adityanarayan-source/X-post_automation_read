# X-post_automation

Minimal FastAPI backend for the X API v2, using the official `xdk` Python SDK.
This first version only reads the authenticated user's profile — no write
operations (posting, deleting, etc.) are implemented yet, but the project is
structured so they can be added later.

## Project structure

```
X-post_automation/
├── app/
│   ├── main.py           # FastAPI app + router registration
│   ├── api/
│   │   ├── users.py       # GET /api/v1/me
│   │   └── health.py      # GET /health
│   ├── services/
│   │   └── x_client.py    # All xdk SDK interaction lives here
│   ├── schemas/
│   │   └── user.py        # Pydantic response models
│   └── core/
│       ├── config.py      # Settings loaded from .env
│       └── exceptions.py  # App-level exceptions
├── tests/
│   └── test_health.py
├── .env.example
├── requirements.txt
└── run.py
```

## Installation

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## .env setup

Copy the example file and fill in your real credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
X_CLIENT_ID=your_client_id
X_CLIENT_SECRET=your_client_secret
X_ACCESS_TOKEN=your_oauth2_user_access_token
X_REFRESH_TOKEN=your_refresh_token
X_REDIRECT_URI=http://localhost:8000/api/v1/auth/x/callback

X_SCOPES=users.read,tweet.read,tweet.write
```

For this first read-only version, only `X_ACCESS_TOKEN` needs to be a valid
OAuth 2.0 User Context access token (scope `users.read` at minimum). The
other fields are captured now so the OAuth flow and token refresh can be
added later without restructuring.

**Never commit your real `.env` file** — it's already in `.gitignore`.

## Running the app

```bash
python run.py
```

The app starts at `http://127.0.0.1:8000` with auto-reload enabled.

Interactive API docs (Swagger UI) are available at:

```
http://127.0.0.1:8000/docs
```

## Testing `/health`

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status": "ok"}
```

## Testing `/api/v1/me`

```bash
curl http://127.0.0.1:8000/api/v1/me
```

Expected response:

```json
{
  "success": true,
  "data": {
    "id": "2244994945",
    "name": "X Developers",
    "username": "XDevelopers",
    "profile_image_url": "https://pbs.twimg.com/profile_images/.../avatar.jpg"
  }
}
```

If `X_ACCESS_TOKEN` is missing or invalid, the endpoint returns a clean
HTTP error (no token or secret is ever included in the response or logs).

## Running unit tests

```bash
pytest
```

## Next steps (not implemented yet)

- `POST /api/v1/posts` — create a post
- `DELETE /api/v1/posts/{post_id}` — delete a post
- `GET /api/v1/posts/{post_id}` — read a post
- Full OAuth 2.0 authorization code flow + token refresh
- Media upload
- MongoDB persistence
