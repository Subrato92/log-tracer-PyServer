from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
import logging

try:
    from ..services import log_service
    from ..database import get_db
except:
    from services import log_service
    from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
        prefix="/log",
        tags=["logging"],
        responses={404: {"description": "Not found"}},
    )

@router.get("/{service_id}/{start_date_time}/{end_date_time}", response_model=list[str])
async def fetch_logs(service_id: Annotated[int, Path(title="Service Id")], 
                     start_date_time: Annotated[datetime, Path(title="Start Date Time")], 
                     end_date_time: Annotated[datetime, Path(title="End Date Time")], 
                     db: Session = Depends(get_db)):
    logs = log_service.get_logs(service_id, start_date_time, end_date_time, db)
    return logs