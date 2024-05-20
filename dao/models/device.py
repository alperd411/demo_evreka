from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, ForeignKey, FLOAT
from sqlalchemy.orm import mapped_column, Mapped, relationship

from dao.common import Base
import alembic

class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    locations = relationship('Location', backref='device',cascade="all,delete")
    last_location_longitude = Column(String)
    last_location_latitude = Column(String)

    def __init__(self, name, last_location_longitude, last_location_latitude):
        self.name = name
        self.last_location_longitude = last_location_longitude
        self.last_location_latitude = last_location_latitude

class Location(Base):
    __tablename__ = "device_location_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(ForeignKey('device.id'))
    longitude = Column(String)
    latitude = Column(String)
    time_stamp = Column(String)


    def __init__(self, longitude, latitude, device_id):
        self.latitude = latitude
        self.longitude = longitude
        self.device_id = device_id
        self.time_stamp = datetime.now(timezone.utc).strftime("%Y/%m/%d, %H:%M:%S")
