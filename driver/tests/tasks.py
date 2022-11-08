from unittest import TestCase
from common.test.test_helper import vcr

from driver.tasks import get_drivers_task
from driver.models import Driver

class DriverTaskTestCase(TestCase):
    def setUp(self):
        pass

    @vcr.use_cassette()
    def test_sucessful_get_drivers_task(self):
        Driver.objects.all().delete()
        self.assertEquals(
            0,
            Driver.objects.count()
        )
        get_drivers_task()
        self.assertGreater(
            Driver.objects.count(),
            10
        )
        driver = Driver.objects.first()
        self.assertIsNotNone(driver.lng)
        self.assertIsNotNone(driver.lat)
        self.assertIsNotNone(driver.last_update)
