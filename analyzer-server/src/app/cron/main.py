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
                file_path_download = run_downloader()
                if not file_path_download or file_path_download == "":
                    return

                file_path_spider = run_spiders()
                if not file_path_spider or file_path_spider == "":
                    return

                is_save_db_success = save_to_db()
                if not is_save_db_success:
                    return

        yield

    app.router.lifespan_context = lifespan
