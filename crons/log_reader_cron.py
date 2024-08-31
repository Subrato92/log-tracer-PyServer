from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import shutil
import logging
import os

try:
    from ..utils.file_utils import getFileMetadata, getArchiveFilepath
    from ..crud import logchunk as crud_logchunk
    from ..crud import cron_job as crud_cron_job
    from ..database import get_db
    from .. import schemas
except:
    from utils.file_utils import getFileMetadata, getArchiveFilepath
    from crud import logchunk as crud_logchunk
    from crud import cron_job as crud_cron_job
    from database import get_db, SessionLocal
    import schemas

logger = logging.getLogger(__name__)

def scheduled_reader(time_seconds):
    db = next(get_db())
    try:
        logger.info("cron job is running...")
        curr_datetime = datetime.now()
        time_change = timedelta(seconds=time_seconds) 
        next_datetime = curr_datetime + time_change
        jobs = crud_cron_job.get_jobs(db, curr_datetime)
        for job in jobs:
            filemetaData = getFileMetadata(job.source_path)
            archiveFilePath = getArchiveFilepath(filemetaData, job.archive_path, str(curr_datetime))
            file_size = os.path.getsize(job.source_path)
            if file_size==0:
                continue
            logger.info("File Size:"+str(file_size)+" bytes")
            shutil.copy(job.source_path, archiveFilePath)
            #os.remove(job.source_path)
            with open(job.source_path, 'w') as file:
                pass

            crud_cron_job.update_job_scheduled_execution_time(db, job, next_datetime)
            crud_logchunk.addChunk(db, schemas.logChunk(logtime=curr_datetime, service_id=job.service_id, archive_path=archiveFilePath))

    except Exception as e:
        logger.error("error in running cronjob - "+ str(e))
        logger.error("Stacktrace - "+ str(e.with_traceback))
    
    db.close()