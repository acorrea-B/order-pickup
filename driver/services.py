import logging

from django.conf import settings
from driver.rest_client import RestClient
from driver.models import Driver

class DriverService():

    def __init__(self):
        api_config = settings.DRIVERS_API_CONFIG
        self.logger = logging.getLogger(__name__)
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

        for driver in driver_list['alfreds']:
            Driver.objects.get_or_create(
                id=driver.get("id"),
                defaults={
                    'lat': int(driver.get('lat', 0)),
                    'lng': int(driver.get('lng', 0)),
                    'last_update': driver.get('lastUpdate')
                }
            )

    def get_nearest_driver(
        self,
        point, date
    ):
        return Driver.objects.filter(
            lat__range=(point, point * 2),
            lng__range=(point, point * 2),
            last_update=date
        ).order_by('lng', 'lat')
    
            