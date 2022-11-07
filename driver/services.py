from urllib import response
from django.conf import settings
from driver.rest_client import RestClient
from driver.models import Driver

class DriverService():
    def __init__(self):
        api_config = settings.DRIVERS_API_CONFIG
        self.client = RestClient(
            base_url=api_config.get('URL', ''),
            timeout=api_config.get('TIMEOUT', 10)
        )
    
    def update_or_create_drivers(self):
        try:
            response = self.client.get_drivers()
        except:
            self.logger.error(
                'Failed to update driver list'
            )
            return
        
        driver_list = response.json()

        for driver in driver_list["alfreds"]:
            driver['last_update'] = driver.get('lastUpdate', None)
            del driver['lastUpdate']
            Driver.objects.update_or_create(
                id=driver.get("id"),
                defaults=driver
            )

        
            