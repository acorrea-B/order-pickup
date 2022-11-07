from django.db import models


class User(models.Model):

    class IdentificationType(models.TextChoices):
        CC = 'CC', _('Cédula de ciudadanía')
        CE = 'CE', _('Cédula de extranjería')
    
    identification_number = models.CharField(
        max_length=20,
        primary_key = True,
        help_text = "unique identification number user's"
    )
    identification_type = models.CharField(
        max_length=2,
        choices=IdentificationType.choices,
        help_text = "identification type user's"
    )
    first_name = models.CharField(
        max_length=150,
        help_text = "names of user"
    )
    last_name = models.CharField(
        max_length=150,
        help_text = "last names of user"
    )
    date_of_issue = models.DateField(
        help_text = "date of issue identification user's"
    )
    birthday = models.DateField(
        help_text = "date of birthday user's"
    )
    email = models.EmailField(
        max_length = 254,
        help_text = "contact via email user's"
    )
    phone_number = models.CharField(
        max_length=15,
        help_text = "contact via phone number user's"
    )

