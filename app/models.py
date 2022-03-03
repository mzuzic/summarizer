import enum

from app.database import Base
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.types import Enum
from sqlalchemy.sql import func


class Status(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = 'finished'
    FAILED = 'failed'


@dataclass
class Request(Base):
    id: int
    summary: str
    time_created: str
    status: str

    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    summary = Column(Text())
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(Status), default=Status.PENDING)

    def __repr__(self):
        return f'Request {self.id} - {self.status}'
