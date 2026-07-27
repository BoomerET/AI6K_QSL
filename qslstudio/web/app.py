from fastapi import FastAPI

from .routes import router as qso_router
from .settings import router as settings_router


app = FastAPI(
    title="AI6K QSL Studio",
    version="0.3.0",
)

app.include_router(qso_router)
app.include_router(settings_router)
