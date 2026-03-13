import json
import subprocess
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="google-tools", version="0.1.0")


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
def calendar_today():
    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    params = {
        "calendarId": "primary",
        "timeMin": start.isoformat().replace("+00:00", "Z"),
        "timeMax": end.isoformat().replace("+00:00", "Z"),
        "singleEvents": True,
        "orderBy": "startTime"
    }
    return run_gws(["calendar", "events", "list", "--params", json.dumps(params)])


@app.get("/gmail/unread")
def gmail_unread(max_results: int = Query(default=10, le=50)):
    params = {"userId": "me", "q": "is:unread", "maxResults": max_results}
    return run_gws(["gmail", "users", "messages", "list", "--params", json.dumps(params)])


@app.get("/drive/search")
def drive_search(q: str, page_size: int = Query(default=10, le=50)):
    params = {"q": q, "pageSize": page_size}
    return run_gws(["drive", "files", "list", "--params", json.dumps(params)])
