from celery import shared_task
from driver.services import DriverService

@shared_task(name = "get_drivers_task")
def get_drivers_task():
    """
        Periodic task that gets a list updated
        of drivers and save in database
    """
    DriverService().update_or_create_drivers()
