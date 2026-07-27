from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from ..services import test_wavelog_connection
from ..wavelog.config import WavelogConfig
from .common import connection_error_message, templates


router = APIRouter(prefix="/settings")


def settings_context(
    request: Request,
    *,
    url: str = "",
    message: str | None = None,
    error_message: str | None = None,
):
    configured = WavelogConfig.is_configured()
    environment_override = WavelogConfig.environment_override_active()

    if not url and configured:
        try:
            url = WavelogConfig.load_effective().url
        except Exception:
            pass

    return {
        "request": request,
        "url": url,
        "configured": configured,
        "environment_override": environment_override,
        "message": message,
        "error_message": error_message,
    }


@router.get("", response_class=HTMLResponse)
def settings(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context=settings_context(request),
    )


@router.post("/test", response_class=HTMLResponse)
def test_settings(
    request: Request,
    wavelog_url: str = Form(...),
    api_key: str = Form(default=""),
):
    try:
        if not api_key.strip():
            api_key = WavelogConfig.load_effective().api_key

        config = WavelogConfig(wavelog_url, api_key)
        version = test_wavelog_connection(config)
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="settings.html",
            context=settings_context(
                request,
                url=wavelog_url,
                error_message=connection_error_message(exc),
            ),
            status_code=400,
        )

    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context=settings_context(
            request,
            url=config.url,
            message=f"Connected successfully to Wavelog {version}.",
        ),
    )


@router.post("")
def save_settings(
    request: Request,
    wavelog_url: str = Form(...),
    api_key: str = Form(default=""),
):
    if WavelogConfig.environment_override_active():
        return templates.TemplateResponse(
            request=request,
            name="settings.html",
            context=settings_context(
                request,
                url=wavelog_url,
                error_message=(
                    "Settings are controlled by WAVELOG_URL and "
                    "WAVELOG_API_KEY environment variables."
                ),
            ),
            status_code=409,
        )

    try:
        if not api_key.strip():
            api_key = WavelogConfig.load_effective().api_key

        config = WavelogConfig(wavelog_url, api_key)
        test_wavelog_connection(config)
        config.save()
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="settings.html",
            context=settings_context(
                request,
                url=wavelog_url,
                error_message=connection_error_message(exc),
            ),
            status_code=400,
        )

    return RedirectResponse(url="/", status_code=303)
