from sqlalchemy.orm import Session
import logging
from datetime import datetime
import shutil

try:
    from ..crud import logchunk as log_crud
    from ..schemas import get_chunk_query
    from ..crud import service
    from ..utils import file_utils
except:
    from crud import logchunk as log_crud
    from schemas import get_chunk_query
    from crud import service
    from utils import file_utils

logger = logging.getLogger(__name__)

null_ch = '\u0000'

def get_logs(service_id: int, start_datetime: datetime, end_datetime: datetime, db: Session) -> list[str]:
    chunk_query = get_chunk_query(service_id=service_id, start_time=start_datetime, end_time=end_datetime)
    logchunks = log_crud.get_chunks(db, chunk_query)

    logs = []
    if logchunks == None:
        return logs

    diff = datetime.now() - end_datetime
    diff_time_sec = diff.total_seconds()

    for logchunk in logchunks:
        logger.info('reading file : '+logchunk.archive_path)
        with open(logchunk.archive_path, 'r') as file:
            for line in file:
                try:
                    lastIdx = line.rindex(null_ch)
                    lastIdx = lastIdx+1
                except:
                    lastIdx = 0
                line = line[lastIdx:]
                line = line.rstrip('\n')
                logger.info('read line: '+line)
                logs.append(line)

    if diff_time_sec < 60:
        service_details = service.get_services_by_id(db, service_id)
        # creating temp file
        tempFilePath = service_details.archive_path + '/temp.out'
        shutil.copy(service_details.source_path, tempFilePath)
        # reading from temp file
        with open(tempFilePath, 'r') as file:
            for line in file:
                try:
                    lastIdx = line.rindex(null_ch)
                    lastIdx = lastIdx+1
                except:
                    lastIdx = 0
                line = line[lastIdx:]
                line = line.rstrip('\n')
                logger.info('read line: '+line)
                logs.append(line)

    return logs