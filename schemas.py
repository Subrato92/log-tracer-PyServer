from pydantic import BaseModel
from datetime import date, datetime

class Path(BaseModel):
    archive_path: str | None = None
    source_path: str | None = None

class ServiceBase(Path):
    id: int | None = None
    name: str
    description: str | None = None

class ApplicationBase(Path):
    id: int | None = None
    name: str
    is_active: bool | None = None
    services: list[ServiceBase] = []

class ServiceCreate(Path):
    name: str
    application_id: int
    description: str | None = None

    def __str__(self) -> str:
        service = {
            "name": self.name,
            "application_id": self.application_id,
            "description": self.description
        }
        return str(service)

class logChunk(Path):
    logtime: datetime
    service_id: int | None = None

class logChunks(BaseModel):
    chunks: list[logChunk] = None

class new_cron_job(Path):
    service_id: int
    scheduled_execution_time: datetime

class entity(BaseModel):
    ids: list[int] = []

class get_chunk_query(BaseModel):
    service_id: int
    start_time: datetime
    end_time: datetime | None = None

class Path(BaseModel):
    path: str