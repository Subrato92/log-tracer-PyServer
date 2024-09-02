from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
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
    from .routers import utils_router
except:
    import models
    from database import engine
    from routers import application as router_application
    from routers import log_router
    from crons import log_reader_cron
    from routers import utils_router

models.Base.metadata.create_all(bind=engine)

def cron_jobs(): 
    cadence = 60
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

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_application.router)
app.include_router(log_router.router)
app.include_router(utils_router.router)