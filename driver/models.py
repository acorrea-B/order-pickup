from django.db import models
from django.core.validators import MaxValueValidator

class Driver(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )
    lat = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        help_text = "location latitude Driver"
    )
    lng = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        help_text = "location longitude Driver"
    )
    last_update = models.DateTimeField()


    
