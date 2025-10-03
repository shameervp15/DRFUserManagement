from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfileModel(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    geneder = models.CharField(
        choices=GENDER_CHOICES, max_length=1, null=True, blank=True
    )
    mobilenumber = models.CharField(
        max_length=10, validators=[RegexValidator(
            regex=r'^\d{10}$', message='Enter a valid 10 digits mobile number.'
        )]
    )

    def __str__(self):
        return self.user.username