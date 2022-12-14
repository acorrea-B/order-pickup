import datetime
from django.utils import timezone
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
            last_update=timezone.now()
        )

class ServicesTestCase(TestCase):

    @vcr.use_cassette()
    def test_create_drivers(self):
        date = "2021-12-10T00:00:00.000Z"
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
        self.assertEquals(
            driver.last_update,
            datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z'),
        )
    
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

    @vcr.use_cassette()
    def test_get_nearest_driver_with_existent_date(self):
        
        DriverService().update_or_create_drivers()
        
        date = "2021-12-10T10:00:00Z"
        point = 10
        result = DriverService().get_nearest_driver(
            point=point, date=date
        )
        self.assertGreater(
            result.count(),
            2
        )

        for item in result:
            self.assertGreaterEqual(
                item.lat,
                point
            )
            self.assertLessEqual(
                item.lat,
                point * 2
            )
            self.assertGreaterEqual(
                item.lng,
                point
            )
            self.assertLessEqual(
                item.lng,
                point * 2
            )
    
    def test_get_nearest_driver_with_no_near_drivers(self):
        date = "2021-12-09T00:00:00Z"
        point = 100 
        result = DriverService().get_nearest_driver(
            point, date
        )
        
        self.assertEqual(
            result.count(),
            0
        )

        