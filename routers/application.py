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
async def create_application(application: ApplicationBase, db: Session = Depends(get_db)):
    try:
        new_application = application_service.create_new_application(application=application, db=db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_application

@router.get("/", response_model=list[ApplicationBase])
async def get_all_applications( db: Session = Depends(get_db)):
    applications = crud_application.getAll(db)
    return applications

@router.get("/{application_id}", response_model=ApplicationBase)
async def get_aplication(application_id: Annotated[int, Path(title="Application Id")], 
                   db: Session = Depends(get_db)):
    application = crud_application.getById(db, application_id)

    if application == None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application

@router.delete("/{application_id}", response_model=ApplicationBase)
async def delete_application(application_id: Annotated[int, Path(title="Application Id")], 
                   db: Session = Depends(get_db)):
    application = application_service.delete_application(application_id, db)

    if application == None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application