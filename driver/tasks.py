from orderpickup.celery import app
from driver.services import DriverService

@app.task
def get_drivers_task():
    """
        Periodic task that gets a list updated
        of drivers and save in database
    """
    DriverService().update_or_create_drivers()
