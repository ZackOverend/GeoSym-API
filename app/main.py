from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.docs import scalar_docs

app = FastAPI(
    title="GeoSym API",
    description="Geological map digitization pipeline",
    version="0.1.0",
    docs_url=None,
)


@app.get("/docs", include_in_schema=False)
async def docs() -> HTMLResponse:
    return scalar_docs()


@app.get("/health")
async def health():
    return {"status": "ok"}
