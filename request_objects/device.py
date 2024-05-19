from pydantic import BaseModel

from dao.models.device import Device


class DeviceRequest(BaseModel):
    name: str
    last_location_longitude: float
    last_location_latitude: float


    def create_device(self):
        return Device(self.name,self.last_location_longitude, self.last_location_latitude)
