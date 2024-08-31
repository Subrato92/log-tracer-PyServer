from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
import logging

try:
    from ..schemas import ApplicationBase
    from ..crud import application as crud_application
    from ..crud import service as crud_service
    from ..database import get_db
    from ..services import application_service
except:
    from schemas import ApplicationBase
    from crud import application as crud_application
    from crud import service as crud_service
    from services import application_service
    from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
        prefix="/application",
        tags=["application"],
        responses={404: {"description": "Not found"}},
    )

@router.post("/", response_model=ApplicationBase)
async def create_item(application: ApplicationBase, db: Session = Depends(get_db)):
    new_application = application_service.create_new_application(application=application, db=db)
    return new_application

@router.get("/", response_model=list[ApplicationBase])
async def get_all( db: Session = Depends(get_db)):
    applications = crud_application.getAll(db)
    return applications

@router.get("/{application_id}", response_model=ApplicationBase)
async def get_item(application_id: Annotated[int, Path(title="Application Id")], 
                   db: Session = Depends(get_db)):
    application = crud_application.getById(db, application_id)

    if application == None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application