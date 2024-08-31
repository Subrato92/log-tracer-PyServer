from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
try:
    from .. import models, schemas
    from ..utils.path_utils import getApplicationArchivePath
except:
    import models, schemas
    from utils.path_utils import getApplicationArchivePath

def getAll(db: Session):
    return db.query(models.Application).all()

def getById(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()

def getByName(db: Session, application_name: str):
    return db.query(models.Application).filter(models.Application.name == application_name).first()

def addApplication(db: Session, application: schemas.ApplicationBase):   
    
    logging.info("Received ApplicationBase:" + str(application))

    db_application = models.Application(name=application.name, archive_path=getApplicationArchivePath(application.name))
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application