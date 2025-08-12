import os
from fastapi import FastAPI
from app.http.main import router
from app.cron.main import register_cron_events
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
import glob

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

    @app.delete("/delete-pngs")
    async def delete_pngs():
        tmp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../tmp"))
        png_files = glob.glob(os.path.join(tmp_dir, "*.png"))
        deleted = []
        for file_path in png_files:
            try:
                os.remove(file_path)
                deleted.append(os.path.basename(file_path))
            except Exception:
                continue
        return {"deleted": deleted, "count": len(deleted)}

elif mode == "cron":
    register_cron_events(app)
