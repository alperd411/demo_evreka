import http.client
import os
import logging

from celery import Celery

from dao.models.device import Device, Location
from dao.repositories.device_repository import DeviceRepository

repo = DeviceRepository()

#create celery
celery = Celery(broker="redis://127.0.0.1:6379")
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


print(celery.connection().info())

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='app.log',
                    level=logging.DEBUG)


class TaskQueue:
    @celery.task(name="test")
    def create_task(name):
        logging.debug("lololo")
        return repo.list_devices()

    @celery.task(name="add_device")
    def add_device(device: Device):
        try:
            created_device = repo.create_device(device)
            logging.info(f'Device Added ID = {device.id}')
            return device.id
        except Exception as e:
            logging.critical(f'Device coul not be added {device},'
                             f'error message => {repr(e)}')
            return http.HTTPStatus.SERVICE_UNAVAILABLE

    @celery.task(name="delete_device")
    def delete_device_byid(id: int):
        try:
            repo.delete_device_byid(id)
            logging.info(f'device deleted with locations')
        except Exception as e:
            logging.error(f'device could not be deleted. deviceId = {id}')
            return http.HTTPStatus.SERVICE_UNAVAILABLE


    @celery.task(name="add_location")
    def add_location_to_device(location:Location):
        try:
            repo.add_location(location)
            logging.info(f'device location arrived {location}')
        except Exception as e:
            logging.error(f'location could not be added {location}, \n err => {repr(e)}')
            return http.HTTPStatus.SERVICE_UNAVAILABLE


def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
            'task-failed': announce_failed_tasks,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


"""


 

"""
