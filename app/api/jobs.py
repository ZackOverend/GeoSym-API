import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import JobResultResponse, JobStatusResponse, JobSubmitResponse
from app.core.config import settings
from app.db.models import Job
from app.db.session import get_db

UPLOAD_DIR = settings.upload_dir
CHUNK_SIZE = 1024 * 1024  # 1MB

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/submit", response_model=JobSubmitResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_job(file: UploadFile, db: AsyncSession = Depends(get_db)) -> JobSubmitResponse:
    safe_filename = Path(file.filename or "").name
    if not safe_filename or not safe_filename.lower().endswith((".tif", ".tiff", ".pdf")):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File must be a GeoTIFF (.tif, .tiff) or scanned map PDF (.pdf)",
        )

    file_id = uuid.uuid4()
    dest = UPLOAD_DIR / str(file_id)  # UUID only — never use user input in file path

    try:
        async with aiofiles.open(dest, "wb") as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
    except Exception:
        dest.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded file",
        )

    try:
        job = Job(id=file_id, filename=safe_filename)
        db.add(job)
        await db.commit()
    except Exception:
        dest.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job record",
        )

    # TODO: enqueue ARQ task here once worker is set up

    return JobSubmitResponse(job_id=job.id, status=job.status)


@router.get("/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> JobStatusResponse:
    row = await db.execute(select(Job).where(Job.id == job_id))
    job = row.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


@router.get("/{job_id}/result", response_model=JobResultResponse)
async def get_job_result(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> JobResultResponse:
    row = await db.execute(select(Job).where(Job.id == job_id))
    job = row.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return JobResultResponse(
        job_id=job.id,
        status=job.status,
        result=job.result,
        error=job.error,
    )
