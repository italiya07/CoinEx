from datetime import date, datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class FearAndGreedIndex(models.Model):
    date = models.DateField()
    value = models.IntegerField()
    def _str_(self):
        return f'{self.date} - {self.value}'

class News(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    published_date = models.DateField(default=date.today)
    def _str_(self):
        return f'{self.title} - {self.published_date}'

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
    id_or_photo = models.ImageField(upload_to='id_or_photo/', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # User._meta.get_field('groups').related_query_name = 'mainApp_user_groups'
    # User._meta.get_field('user_permissions').related_query_name = 'mainApp_user_permissions'

    def _str_(self):
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
    launch_date = models.DateField(null=True, blank=True, default=date.today)


    def _str_(self):
        return self.name

class ContactUs(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_email = models.CharField(max_length=200)
    query = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def _str_(self):
        return f'{self.customer_name} - {self.created_at}'
    

class Transaction(models.Model):
    TYPE = [("BUY", "Buy"), ("SELL", "Sell")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TYPE, default="BUY")
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)  # Assuming you have a Crypto model


    def __str__(self):
        return f"{self.user.email} - {self.transaction_type}{self.quantity} {self.crypto.symbol} @ {self.price}"

class NFT(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    image = models.ImageField(upload_to="nft_images/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)

class NFTTransaction(models.Model):
    TYPE = [("BUY", "Buy"), ("SELL", "Sell")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TYPE, default="BUY")
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)  # Assuming you have a Crypto model


    def __str__(self):
        return f"{self.user.email} - {self.transaction_type}{self.quantity} {self.crypto.symbol} @ {self.price}"