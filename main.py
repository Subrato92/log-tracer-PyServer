from typing import Union
from fastapi import FastAPI, Depends
from fastapi_utilities import repeat_every
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import logging
import logging.config
import time
import threading
import sys

# logging.config.fileConfig('logging.conf')
# log = logging.getLogger('consoleHandler')

log = logging.getLogger(__name__)

try:
    from . import models
    from .database import engine
    from .routers import application as router_application
    from .routers import log_router
    from .crons import log_reader_cron
except:
    import models
    from database import engine
    from routers import application as router_application
    from routers import log_router
    from crons import log_reader_cron

models.Base.metadata.create_all(bind=engine)

def cron_jobs(): 
    cadence = 600
    while 1:
        log_reader_cron.scheduled_reader(cadence)
        time.sleep(cadence)

@asynccontextmanager
async def lifespan(app: FastAPI): 
    log.info("Initializing cron jobs...")
    worker_thread = threading.Thread(target=cron_jobs)
    worker_thread.start()

    yield
    log.info("All cron jobs killed...")
    
app = FastAPI(lifespan=lifespan)

app.include_router(router_application.router)
app.include_router(log_router.router)