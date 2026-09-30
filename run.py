"""
Simple entrypoint to run the app with Uvicorn:

    python run.py
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
