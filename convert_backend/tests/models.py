"""Models for test suite."""
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import  relationship

model_metadata = MetaData()
Base = declarative_base(metadata = model_metadata)

class Cloud(Base):
    """A group of machines connected in a cloud."""
    __tablename__ = 'cloud'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __str__(self):
        return self.name


class Machine(Base):
    """A single machine which is part of a cloud deployment."""
    __tablename__ = 'machine'

    id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable=False)
    operating_system = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cloud_id = Column(Integer, ForeignKey('cloud.id'))
    cloud = relationship('Cloud')
    is_running = Column(Boolean, default=False, nullable=False)
    last_started_at = Column(DateTime, default=datetime.datetime.now())

    def __str__(self):
        """Return string representation."""
        return self.hostname