from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from datetime import datetime

try:
    from .. import models, schemas
except:
    import models, schemas

def add_job(db: Session, cron_job: schemas.new_cron_job):
    db_cronjob = models.cron_jobs(
        archive_path=cron_job.archive_path, 
        source_path=cron_job.source_path, 
        scheduled_execution_time=cron_job.scheduled_execution_time, 
        service_id=cron_job.service_id)
    db.add(db_cronjob)
    db.commit()
    db.refresh(db_cronjob)
    return db_cronjob

def update_job_scheduled_execution_time(db: Session, job: models.cron_jobs, next_execution_time: datetime) -> bool:
    stmt = update(models.cron_jobs).where(models.cron_jobs.id==job.id).values(scheduled_execution_time=next_execution_time)
    db.execute(stmt)
    db.commit()
    return True

def delete_job(db: Session, service_ids: schemas.entity) -> bool:
    for id in service_ids.ids:
        stmt = delete(models.cron_jobs).where(models.cron_jobs.id==id)
        db.execute(stmt)
        db.commit()

    return True

def get_jobs(db: Session, currDateTime: datetime) -> list[models.cron_jobs]:
    return db.query(models.cron_jobs)\
            .filter(models.cron_jobs.scheduled_execution_time <= currDateTime).all()