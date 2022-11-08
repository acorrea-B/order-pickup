import datetime
import requests_mock

from unittest import TestCase
from common.test.test_helper import vcr
from driver.models import Driver
from driver.services import DriverService

def generate_drivers():
    for i in range(0, 13):
        Driver.objects.create(
            lat=0,
            lng=0,
            last_update=datetime.timezone.utc
        )

class ServicesTestCase(TestCase):

    @vcr.use_cassette()
    def test_create_drivers(self):
        Driver.objects.all().delete()
        self.assertEquals(
            0,
            Driver.objects.count()
        )
        DriverService().update_or_create_drivers()
        self.assertGreater(
            Driver.objects.count(),
            10
        )
        driver = Driver.objects.first()
        self.assertIsNotNone(driver.lng)
        self.assertIsNotNone(driver.lat)
        self.assertIsNotNone(driver.last_update)
    
    @vcr.use_cassette()
    def test_update_drivers(self):
        Driver.objects.all().delete()
        generate_drivers()
        self.assertEquals(
            13,
            Driver.objects.count()
        )
        existent_driver = Driver.objects.first()
        DriverService().update_or_create_drivers()
        self.assertGreater(
            Driver.objects.count(),
            10
        )
        driver = Driver.objects.first()
        self.assertNotEquals(
            existent_driver.lng,
            driver.lng
        )
        self.assertNotEquals(
            existent_driver.lat,
            driver.lat
        )
        self.assertNotEquals(
            existent_driver.last_update,
            driver.last_update
        )
    
    @requests_mock.Mocker(real_http=True)
    def test_falied_update_or_create_drivers(self, mock):
        mocked_url = 'https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json'
        mock.get(
            mocked_url,
            status_code=200
        )
        Driver.objects.all().delete()
        self.assertEquals(
            0,
            Driver.objects.count()
        )
        with self.assertLogs(
            logger='driver.services',
            level='ERROR'
        ) as cm:
            DriverService().update_or_create_drivers()
        
        self.assertIn(
            'Failed to update driver list',
            cm.output[0].split('\\n')[0]
        )     
        self.assertEquals(
            0,
            Driver.objects.count()
        )
        