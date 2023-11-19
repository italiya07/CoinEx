from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    today_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class FearAndGreedIndex(models.Model):
    date = models.DateField()
    value = models.IntegerField()
    def __str__(self):
        return f'{self.date} - {self.value}'

class News(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    def __str__(self):
        return self.title




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        if 'first_name' not in extra_fields:
            raise ValueError('You must provide a first name')
        if 'last_name' not in extra_fields:
            raise ValueError('You must provide a last name')

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
# class User(AbstractBaseUser):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # User._meta.get_field('groups').related_query_name = 'mainApp_user_groups'
    # User._meta.get_field('user_permissions').related_query_name = 'mainApp_user_permissions'

    def __str__(self):
        return self.email


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    one_hour_change = models.DecimalField(max_digits=5, decimal_places=2)
    one_hour_flag = models.IntegerField()
    twenty_four_hour_change = models.DecimalField(max_digits=5, decimal_places=2)
    twenty_four_hour_flag = models.IntegerField()
    market_cap = models.BigIntegerField()
    volume = models.BigIntegerField()

    def __str__(self):
        return self.name
