import os
from fastapi import FastAPI
from app.http.main import router
from app.cron.main import register_cron_events
from fastapi.staticfiles import StaticFiles

app = FastAPI()

mode = os.getenv("APP_MODE", "http")

if mode == "http":
    app.include_router(router, prefix="/api/v1", tags=["Analyzer"])

    app.mount(
        "/public",
        StaticFiles(
            directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "../tmp"))
        ),
        name="public",
    )

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

elif mode == "cron":
    register_cron_events(app)
