from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import BackgroundTasks, FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from ..services import fetch_recent_qsos, generate_back_pdf


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


@app.post("/generate")
def generate_selected_qsl_cards(
    background_tasks: BackgroundTasks,
    selected_qsos: list[int] = Form(default=[]),
):
    if not selected_qsos:
        raise HTTPException(
            status_code=400,
            detail="Select at least one QSO before generating a PDF.",
        )

    try:
        profile, qsos = fetch_recent_qsos(limit=50)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve Wavelog contacts: {exc}",
        ) from exc

    unique_indexes = list(dict.fromkeys(selected_qsos))
    invalid_indexes = [
        index
        for index in unique_indexes
        if index < 0 or index >= len(qsos)
    ]
    if invalid_indexes:
        raise HTTPException(
            status_code=400,
            detail="The QSO list changed. Refresh the page and try again.",
        )

    selected = [qsos[index] for index in unique_indexes]

    with NamedTemporaryFile(
        prefix="ai6k-qsl-",
        suffix=".pdf",
        delete=False,
    ) as temporary_file:
        output_path = Path(temporary_file.name)

    try:
        generate_back_pdf(selected, profile, output_path)
    except Exception:
        output_path.unlink(missing_ok=True)
        raise

    background_tasks.add_task(output_path.unlink, missing_ok=True)

    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename="AI6K-QSL-cards.pdf",
        background=background_tasks,
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": "AI6K QSL Studio",
    }

