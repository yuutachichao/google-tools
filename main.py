import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Query

app = FastAPI(title="google-tools", version="0.2.0")

API_KEY = os.getenv("API_KEY")


def require_api_key(authorization: Optional[str]):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not configured")

    expected = f"Bearer {API_KEY}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")


def run_gws(args):
    result = subprocess.run(["gws", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr or result.stdout)

    try:
        return json.loads(result.stdout)
    except Exception:
        return {"raw": result.stdout}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/calendar/today")
def calendar_today(authorization: Optional[str] = Header(default=None)):
    require_api_key(authorization)

    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    end = start + timedelta(days=1)

    params = {
        "calendarId": "primary",
        "timeMin": start.isoformat().replace("+00:00", "Z"),
        "timeMax": end.isoformat().replace("+00:00", "Z"),
        "singleEvents": True,
        "orderBy": "startTime",
    }
    return run_gws(["calendar", "events", "list", "--params", json.dumps(params)])


@app.get("/gmail/unread")
def gmail_unread(
    max_results: int = Query(default=10, le=50),
    authorization: Optional[str] = Header(default=None),
):
    require_api_key(authorization)

    params = {"userId": "me", "q": "is:unread", "maxResults": max_results}
    return run_gws(["gmail", "users", "messages", "list", "--params", json.dumps(params)])


@app.get("/drive/search")
def drive_search(
    q: str,
    page_size: int = Query(default=10, le=50),
    authorization: Optional[str] = Header(default=None),
):
    require_api_key(authorization)

    params = {"q": q, "pageSize": page_size}
    return run_gws(["drive", "files", "list", "--params", json.dumps(params)])
