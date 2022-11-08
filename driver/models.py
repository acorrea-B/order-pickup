from django.db import models

class Driver(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )
    lat = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
        help_text = "location latitude Driver"
    )
    lng = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
        help_text = "location longitude Driver"
    )
    last_update = models.DateTimeField()


    
