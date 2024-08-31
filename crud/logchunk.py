from sqlalchemy.orm import Session
from sqlalchemy import delete

try:
    from .. import models, schemas
except:
    import models, schemas

def addChunk(db: Session, logChunk: schemas.logChunk):
    db_logchunk = models.LogChunks(archive_path=logChunk.archive_path, logtime=logChunk.logtime, service_id=logChunk.service_id)
    db.add(db_logchunk)
    db.commit()
    db.refresh(db_logchunk)
    return db_logchunk

def get_chunks(db: Session, query: schemas.get_chunk_query):
    return db.query(models.LogChunks)\
            .filter(
                models.LogChunks.service_id == query.service_id, 
                models.LogChunks.logtime > query.start_time,
                models.LogChunks.logtime < query.end_time)\
            .all()

def delete_chunks(db: Session, service_id: int):
    stmt = delete(models.LogChunks).where(models.LogChunks.service_id == service_id)
    db.execute(stmt)
    db.commit()