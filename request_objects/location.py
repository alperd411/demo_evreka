from pydantic import BaseModel
import datetime

from dao.models.device import Location
class LocationRequest(BaseModel):
    longitude:str
    latitude:str
    def crete_location(self,device_id : int):
        #date = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        return Location(self.longitude, self.latitude, device_id)






