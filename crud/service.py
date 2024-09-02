from sqlalchemy.orm import Session
from sqlalchemy import delete
import logging

logger = logging.getLogger(__name__)

try:
    from .. import models, schemas
    from ..utils.path_utils import getServiceArchivePath
except:
    import models, schemas
    from utils.path_utils import getServiceArchivePath

def get_services_by_application_id(db: Session, application_id: int):
    return db.query(models.Service).filter(models.Service.application_id == application_id).all()

def get_services_by_application_id_service_name(db: Session, application_id: int, service_name:str):
    return db.query(models.Service).filter(models.Service.name == service_name, models.Service.application_id == application_id).first()

def get_services_by_id(db: Session, service_id: str):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def create_service(db: Session, serviceBase: schemas.ServiceCreate, applicationName: str, application_id:int):
    logging.info("Received ServiceBase:" + str(serviceBase))

    db_service = models.Service(
        name=serviceBase.name, 
        description=serviceBase.description, 
        archive_path=getServiceArchivePath(serviceBase.name, applicationName),
        source_path=serviceBase.source_path,
        application_id=application_id
    )
        
    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service

def delete_services(db: Session, service_ids: schemas.entity) -> bool:
    for id in service_ids:
        stmt = delete(models.Service).where(models.Service.id==id)
        db.execute(stmt)
        db.commit()

    return True