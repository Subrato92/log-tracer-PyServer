from sqlalchemy.orm import Session
import logging
from datetime import datetime

try:
    from ..crud import logchunk as log_crud
    from ..schemas import get_chunk_query
except:
    from crud import logchunk as log_crud
    from schemas import get_chunk_query

logger = logging.getLogger(__name__)

null_ch = '\u0000'

def get_logs(service_id: int, start_datetime: datetime, end_datetime: datetime, db: Session) -> list[str]:
    chunk_query = get_chunk_query(service_id=service_id, start_time=start_datetime, end_time=end_datetime)
    logchunks = log_crud.get_chunks(db, chunk_query)

    logs = []
    if logchunks == None:
        return logs

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

    return logs