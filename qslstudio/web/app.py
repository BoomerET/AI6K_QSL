from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..services import fetch_recent_qsos


WEB_ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = WEB_ROOT / "templates"

app = FastAPI(
    title="AI6K QSL Studio",
    version="0.1.0",
)

templates = Jinja2Templates(directory=str(TEMPLATE_ROOT))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    error_message: str | None = None
    profile = None
    qsos = []

    try:
        profile, qsos = fetch_recent_qsos(limit=50)
    except Exception as exc:
        error_message = str(exc)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": profile,
            "qsos": qsos,
            "error_message": error_message,
        },
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": "AI6K QSL Studio",
    }

