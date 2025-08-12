from fastapi_utilities import repeat_every
from downloader.main import run_downloader
from spiders.main import run_spiders
from db.main import save_to_db
import datetime
from fastapi import FastAPI


from contextlib import asynccontextmanager


def register_cron_events(app: FastAPI):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        @repeat_every(seconds=24 * 60 * 60, wait_first=True)  # Check every day
        async def get_data_job() -> None:
            now = datetime.datetime.utcnow()
            if now.hour == 0 and now.minute == 0:
                run_downloader()
                run_spiders()
                save_to_db()

        yield

    app.router.lifespan_context = lifespan
