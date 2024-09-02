from sqlalchemy.orm import Session
from datetime import datetime
import logging
import shutil

logger = logging.getLogger(__name__)
try:
    from .. import schemas
    from ..crud import application as crud_application
    from ..crud import service as crud_service
    from ..crud import cron_job as crud_cron_job
    from ..utils import path_utils
except: 
    import schemas
    from crud import application as crud_application
    from crud import service as crud_service
    from crud import cron_job as crud_cron_job
    from utils import path_utils

def create_new_application(application: schemas.ApplicationBase, db: Session):
    try:
        new_application = crud_application.getByName(db, application.name)
        if new_application == None:            
            new_application = crud_application.addApplication(db, application)
        
        services = []
        for service in application.services:
            if service == None:
                continue
            service_data = crud_service.get_services_by_application_id_service_name(db, new_application.id, service.name)
            if service_data == None:
                service_data = crud_service.create_service(db, service, new_application.name, new_application.id)
                resp = path_utils.makeDir(service_data.archive_path)
                if resp :
                    cron_job = schemas.new_cron_job(
                        archive_path=service_data.archive_path, 
                        source_path=service_data.source_path, 
                        service_id=service_data.id,
                        scheduled_execution_time=datetime.now())
                    
                    cron_job = crud_cron_job.add_job(db, cron_job)
                    
                    logger.info("Created Job:"+str(cron_job))

            services.append(service_data)
        
        new_application.services = services

        return new_application
    except Exception as e:
        raise Exception(str(e.with_traceback))
    

def delete_application( application_id: int, db: Session):
    application = crud_application.getById(db, application_id)

    if application == None:
        return
    
    service_ids = []
    for service in application.services:
        service_ids.append(service.id)

    if len(service_ids) > 0:
        crud_cron_job.delete_job(db, service_ids)
        crud_service.delete_services(db, service_ids)
    try:
        shutil.rmtree(application.archive_path)
    except FileNotFoundError:
        pass
    except Exception as e:
        raise Exception(str(e.with_traceback()))
    crud_application.delete_application(db, application_id)

    return application