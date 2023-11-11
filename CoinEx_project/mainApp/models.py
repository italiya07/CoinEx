from django.db import models

class Crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    today_price = models.DecimalField(max_digits=10, decimal_places=2)
