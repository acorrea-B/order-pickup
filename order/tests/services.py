import datetime

from unittest import TestCase
from django.utils import timezone
from order.models import Order

from order.services import OrderService
from driver.models import Driver

def generate_orders(driver):
    date = "2021-12-10T00:00:00.000Z"
    creation_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')
    for i in range(0, 13):
        creation_date += datetime.timedelta(hours=1)
        Order.objects.create(
            driver=driver,
            order_date=timezone.now(),
            creation_date=creation_date,
            lat_origin=4,
            lng_origin=6,
            lat_destination=9,
            lng_destination=7
        )

class OrderServiseTestCase(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create(
            lat=6,
            lng=7,
            last_update=timezone.now()
        )

    def test_create_new_order(self):
        result, message = OrderService().create_order(
            driver=self.driver.id,
            order_date=timezone.now() + datetime.timedelta(hours=1),
            lat_origin=4,
            lng_origin=6,
            lat_destination=9,
            lng_destination=7
        )

        self.assertIsInstance(
            result,
            Order
        )
        self.assertEqual(
            message,
            "Orden registrada con éxito"
        )
    
    def test_failcreate_new_order_far_driver(self):
        result, message = OrderService().create_order(
            driver=self.driver.id,
            order_date=timezone.now() + datetime.timedelta(hours=1),
            lat_origin=2,
            lng_origin=3,
            lat_destination=9,
            lng_destination=7
        )

        self.assertIsNone(
            result
        )
        self.assertEqual(
            message,
            "Upsss, estas muy lejos del conductor elegido, intenta nuevamente con otro conductor"
        )
    
    def test_get_orders_by_date(self):
        generate_orders(self.driver)
        self.assertGreater(
            Order.objects.count(),
            10
        )
        
        date = "2021-12-10"
        result = OrderService().get_orders_by_date(
            date=date,
        )

        self.assertGreater(
            result.count(),
            2
        )
        self.assertGreater(
            result.last().creation_date.hour,
            result.first().creation_date.hour
        )
        self.assertEquals(
            result.last().creation_date.day,
            result.first().creation_date.day
        )
    
    def test_get_orders_by_driver_and_date(self):
        new_driver = Driver.objects.create(
            lat=10,
            lng=7,
            last_update=timezone.now()
        )
        generate_orders(new_driver)
        self.assertGreater(
            Order.objects.count(),
            10
        )
        
        date = "2021-12-10"
        result = OrderService().get_orders_by_driver_and_date(
            date=date,
            driver=new_driver.id
        )

        self.assertGreater(
            result.count(),
            2
        )
        self.assertGreater(
            result.last().creation_date.hour,
            result.first().creation_date.hour
        )
        self.assertEquals(
            result.last().creation_date.day,
            result.first().creation_date.day
        )
        self.assertEqual(
            result.last().driver,
            new_driver
        )
        self.assertEqual(
            result.first().driver,
            new_driver
        )

        