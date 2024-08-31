from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
try:
    from .database import Base
except:
    from database import Base

class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    archive_path = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    services = relationship("Service", back_populates="application")


class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    archive_path = Column(String, unique=True, index=True)
    source_path = Column(String, unique=True, index=True)
    application_id = Column(Integer, ForeignKey("application.id"))

    application = relationship("Application", back_populates="services")


class LogChunks(Base):
    __tablename__ = "log_chunks"

    id = Column(Integer, primary_key=True)
    archive_path = Column(String, unique=True, index=True)
    logtime = Column(DateTime, index=True)
    service_id = Column(Integer, ForeignKey("service.id"))


class cron_jobs(Base):
    __tablename__ = "cron_jobs"

    id = Column(Integer, primary_key=True)
    archive_path = Column(String, index=True)
    source_path = Column(String, unique=True, index=True)
    scheduled_execution_time = Column(DateTime, index=True)
    service_id = Column(Integer, ForeignKey("service.id"))

    def __str__(self) -> str:
        job = { 
            "id": self.id, 
            "archive_path": self.archive_path,
            "source_path": self.source_path,
            "scheduled_execution_time": self.scheduled_execution_time,
            "service_id": self.service_id
        }
        return str(job)