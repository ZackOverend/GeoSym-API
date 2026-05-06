import uuid
from datetime import datetime

from pydantic import BaseModel

from app.enums import JobStatus


class JobSubmitResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus


class JobStatusResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus
    created_at: datetime
    updated_at: datetime


class JobResultResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus
    result: dict | None
    error: str | None
