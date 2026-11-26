from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator,RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.
class User(AbstractUser):
    pass 

class Doctor(User):

    license_number =models.CharField(max_length=100,unique=True,validators=[MinLengthValidator(6),MaxLengthValidator(6)])#obligatoirement max_length pour la creation du base de donnée sinon il provoque un erreur
    phone = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    specialities = models.ManyToManyField("AccountApp.Specialty", related_name="doctors")
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

number_validator = RegexValidator(
            regex=r'^\d{8}$',
            message='This number must contain 8 digits'
        )

def validate_birth_date(v):
    if v > timezone.localdate():
        raise ValidationError("Birth date is not valid")

class Patient(User):
    national_id = models.CharField(max_length=8,unique=True,validators=[number_validator])
    phone = models.CharField(max_length=8,validators=[number_validator])
    birth_date = models.DateField(validators=[validate_birth_date])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

class Specialty(models.Model):
    name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"
    def __str__(self):
        return self.name

    
    
