import enum

from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.types import Enum
from sqlalchemy.sql import func


class Status(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = 'finished'
    FAILED = 'failed'


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    model_name = Column(String(50), unique=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(Status), default=Status.PENDING)

    def __repr__(self):
        return f'Request {self.id} - {self.status}'
