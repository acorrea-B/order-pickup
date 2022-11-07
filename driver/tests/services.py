import datetime
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