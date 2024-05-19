from ..common import session_factory
from ..models.device import Device, Location

class DeviceRepository:
    def __init__(self):
        self.session = session_factory()

    def create_device(self, device: Device):
        self.session.add(device)
        self.session.commit()
        self.session.flush()
        id = device.id
        self.session.close()
        return id

    def list_devices(self):
        return self.session.query(Device).all()

    ##update devices last location and add relational location object
    def add_location(self, location: Location):
        device_to_update = self.session.query(Device).get(location.device_id)
        device_to_update.last_location_longitude = location.longitude
        device_to_update.last_location_latitude = location.latitude
        device_to_update.locations.append(location)
        self.session.commit()
        self.session.close()

     #cascadeType includes delete type. so all child entities will deleted
    def delete_device_byid(self,device_id: int):
        self.session.query(Location).filter_by(device_id = device_id).delete()
        self.session.flush()
        #orphan removal? alternatively i can mark all these as removed in db. but that was not specified in case!
        self.session.query(Device).filter_by(id=device_id).delete()
        self.session.commit();
        self.session.close()

    def locations_by_deviceid(self,device_id:int):
        device = self.session.query(Device).get(device_id)
        #because its lazy loading i have to get location attribute
        device.locations
        return device

    def get_lastlocation_byid(self,device_id:int):
        # last location points stored in parent entity table for quick access.
        self.session.query(Device).get(device_id)






