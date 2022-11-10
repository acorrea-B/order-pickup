import datetime

from order.models import Order
from driver.models import Driver


class OrderService:

    def create_order(
        self,
        driver, order_date,
        lat_origin, lng_origin,
        lat_destination, lng_destination
    ):
        driver = Driver.objects.get(id=driver)
        if driver.lat in range(lat_origin, lat_origin * 2 ) and \
            driver.lng in range(lng_origin, lng_origin * 2):

            new_order = Order(
                driver=driver,
                order_date=order_date,
                lat_origin=lat_origin,
                lng_origin=lng_origin,
                lat_destination=lat_destination,
                lng_destination=lng_destination
            )
            
            new_order.full_clean()
            new_order.save()
            return new_order, "Orden registrada con éxito"
        return None, "Upsss, estas muy lejos del conductor elegido, intenta nuevamente con otro conductor"
    
    def get_orders_by_date(self, date):
        date=datetime.datetime.strptime(date, '%Y-%m-%d')
        return Order.objects.filter(
            creation_date__year=date.year,
            creation_date__month=date.month,
            creation_date__day=date.day
        ).order_by('creation_date__hour')
    
    def get_orders_by_hour(self, date):
        date=datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        return Order.objects.filter(
            creation_date__year=date.year,
            creation_date__month=date.month,
            creation_date__day=date.day,
            creation_date__hour=date.hour,
        )
    
    def get_orders_by_driver_and_date(self, date, driver):
        date=datetime.datetime.strptime(date, '%Y-%m-%d')
        return Order.objects.filter(
            creation_date__year=date.year,
            creation_date__month=date.month,
            creation_date__day=date.day,
            driver__id=driver
        ).order_by('creation_date__hour')

