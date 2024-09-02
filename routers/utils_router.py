from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
import logging
import os

try:
    from ..services import log_service
    from ..database import get_db
    from .. import schemas
except:
    from services import log_service
    from database import get_db
    import schemas

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/utilities",
    tags=["utilities"],
    responses={404: {"description": "Not found"}},
)

@router.post("/validate/path")
async def validate_path(path: schemas.Path):
    try:
        logger.info("Path: "+path.path )
        isFile = os.path.isfile(path.path)
        logger.info("Path: "+path.path+", isFile:"+str(isFile) )
        if not isFile:
            raise HTTPException(status_code=404, detail="Invalid Path")
        
        return True
    except Exception as e:
        logger.info("Path: "+path.path+", exception:"+str(e) )
        raise HTTPException(status_code=404, detail="Invalid Path")