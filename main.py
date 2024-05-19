import os

import uvicorn
from fastapi import FastAPI


import celery
from celery import Celery


from dao.repositories.device_repository import DeviceRepository
from request_objects.device import DeviceRequest
from request_objects.location import LocationRequest

from task_queue.worker import TaskQueue





#http://localhost:8001/docs (swagger)
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})

repo = DeviceRepository()
queue = TaskQueue()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/device")
async def save_device(request: DeviceRequest):
    device= request.create_device()
    return queue.add_device(device)

@app.get("/all")
async def list_devices():
    return repo.list_devices()

@app.get("/device/{device_id}")
async def last_location_byid(device_id:int):
    return repo.get_lastlocation_byid(device_id);
@app.get("/device/{device_id}")
async def histroy_by_deviceid(device_id:int):
    return repo.locations_by_deviceid(device_id)


@app.post("/location/{device_id}")
async def add_location_by_device_id(device_id: int, location: LocationRequest):
    location_obj = location.crete_location({device_id})
    queue.add_location_to_device(location_obj)
    return location_obj


@app.delete("/device/{device_id}")
async def delete_device_byid(device_id: int):
    repo.delete_device_byid(device_id)

@app.get("/test")
async def celery_test():
    return queue.create_task("alper")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)

