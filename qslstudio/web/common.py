from pathlib import Path

from fastapi.templating import Jinja2Templates
import requests


WEB_ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = WEB_ROOT / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_ROOT))


def connection_error_message(exc: Exception) -> str:
    if isinstance(exc, requests.Timeout):
        return "Wavelog did not respond before the connection timed out."

    if isinstance(exc, requests.ConnectionError):
        return "The Wavelog server could not be reached."

    if isinstance(exc, requests.HTTPError):
        status_code = exc.response.status_code if exc.response else None
        if status_code in {401, 403, 404}:
            return "Wavelog rejected the URL or API key."
        return f"Wavelog returned HTTP {status_code or 'error'}."

    return str(exc)
