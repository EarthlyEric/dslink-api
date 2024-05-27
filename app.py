from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import Config

config = Config()

app = FastAPI(title="DSLink API",
            version=config.version,
            description="A RESTful API for Luminara.",
            docs_url="/docs",
            redoc_url=None
            )

app.mount("/static", StaticFiles(directory="web/static",html=True), name="static")

from router import web

app.include_router(web.web)

