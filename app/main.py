from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.jobs import router as jobs_router
from app.core.config import settings
from app.docs import scalar_docs


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="GeoSym API",
    description="Geological map digitization pipeline",
    version="0.1.0",
    docs_url=None,
    lifespan=lifespan,
)

app.include_router(jobs_router)


@app.get("/docs", include_in_schema=False)
async def docs() -> HTMLResponse:
    return scalar_docs()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
