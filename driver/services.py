import logging
import math

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
                    'lat': driver.get('lat', 0),
                    'lng': driver.get('lng', 0),
                    'last_update': driver.get('lastUpdate')
                }
            )

    def get_nearest_driver(
        self,
        lat_origin, long_origin,
        lat_limit, long_limit,
        date
    ):

        radius = self.point_distance(
            lat_origin, long_origin,
            lat_limit, long_limit
        )
        return Driver.objects.filter(
            lat__lte=radius,
            lng__lte=radius,
            last_update=date
        )
    
    def point_distance(self, x1, y1, x2, y2):
        radius = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return radius
            