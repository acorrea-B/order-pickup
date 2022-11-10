from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

from driver.models import Driver

class Order(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    creation_date=models.DateTimeField(
        default=timezone.now()
    )
    order_date=models.DateTimeField()
    lat_origin = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        help_text = "location latitude origin order"
    )
    lng_origin = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        help_text = "location longitude origin order"
    )
    lat_destination = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        help_text = "location latitude destination order"
    )
    lng_destination = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        help_text = "location longitude destination order"
    )
    driver = models.ForeignKey(
       Driver,
       on_delete=models.CASCADE,
    )