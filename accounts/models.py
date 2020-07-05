from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self, birth, job, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        # if not email:
        #     raise ValueError('Users must have an email address')

        user = self.model(
            # email=self.normalize_email(email),
            job=job,
            birth=birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
#from phonenumber_field.modelfields import PhoneNumberField
def validate_not_empty(value):
    if value == '':
        return ValidationError('not null error')
    else:
        return value

class User(AbstractUser):
    #phone = PhoneNumberField(null=False, blank=False, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    birth = models.DateField(null=True, blank=True)
    job = models.CharField(max_length=50, blank=True)
    # objects = UserManager()
    REQUIRED_FIELDS = ['phone', 'birth', 'job']

class Point(models.Model):
    #(적립, 소모) 건 by 건으로 저장.
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    occurpoint = models.IntegerField()
    occurdate = models.DateField(auto_now_add=True)
