from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

from ..print_profiles import (
    get_default_print_profile_id,
    get_print_profile,
    list_print_profiles,
)
from ..services import fetch_recent_qsos, generate_back_pdf
from ..wavelog.config import WavelogConfig
from .common import connection_error_message, templates


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    if not WavelogConfig.is_configured():
        return RedirectResponse(url="/settings", status_code=303)

    error_message: str | None = None
    profile = None
    qsos = []

    try:
        profile, qsos = fetch_recent_qsos(limit=50)
    except Exception as exc:
        error_message = connection_error_message(exc)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": profile,
            "qsos": qsos,
            "error_message": error_message,
            "print_profiles": list_print_profiles(),
            "default_print_profile_id": get_default_print_profile_id(),
        },
    )


@router.post("/generate")
def generate_selected_qsl_cards(
    background_tasks: BackgroundTasks,
    selected_qsos: list[int] = Form(default=[]),
    print_profile_id: str = Form(default=""),
):
    if not WavelogConfig.is_configured():
        return RedirectResponse(url="/settings", status_code=303)

    if not selected_qsos:
        raise HTTPException(
            status_code=400,
            detail="Select at least one QSO before generating a PDF.",
        )

    selected_profile_id = print_profile_id or get_default_print_profile_id()

    try:
        print_profile = get_print_profile(selected_profile_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=400,
            detail="The selected print profile is not available.",
        ) from exc

    try:
        profile, qsos = fetch_recent_qsos(limit=50)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "Unable to retrieve Wavelog contacts: "
                f"{connection_error_message(exc)}"
            ),
        ) from exc

    unique_indexes = list(dict.fromkeys(selected_qsos))
    invalid_indexes = [
        index for index in unique_indexes if index < 0 or index >= len(qsos)
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
        generate_back_pdf(
            selected,
            profile,
            output_path,
            print_profile_id=print_profile.profile_id,
        )
    except Exception:
        output_path.unlink(missing_ok=True)
        raise

    background_tasks.add_task(output_path.unlink, missing_ok=True)

    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename=print_profile.effective_download_filename,
        background=background_tasks,
    )


@router.get("/health")
def health():
    return {
        "status": "ok",
        "application": "AI6K QSL Studio",
        "wavelog_configured": WavelogConfig.is_configured(),
        "default_print_profile": get_default_print_profile_id(),
    }
