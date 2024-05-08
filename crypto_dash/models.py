from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Symbols(models.model):
    # Primary key
    id = models.CharField(primary_key=True, max_length=20)

    # Attributes
    name = models.CharField(max_length=20, unique=True)

class Exchanges(models.model):
    # Primary key
    id = models.CharField(primary_key=True, max_length=20)

    # Attributes
    name = models.CharField(max_length=20, unique=True)

class Records(models.model):
    # Primary key
    id = models.AutoField(primary_key=True)

    # Foreign keys
    symbol = models.ForeignKey(Symbols, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchanges, on_delete=models.CASCADE)

    # Attributes
    price_open = models.FloatField()
    price_close = models.FloatField()
    price_low = models.FloatField()
    price_high = models.FloatField()
    time_open = models.DateTimeField()
    time_close = models.DateTimeField()

class Transactions(models.model):
    # Primary key
    id = models.AutoField(primary_key=True)

    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbols, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchanges, on_delete=models.CASCADE)

    type_choice = {
        'B': "BUY",
        'S': "SELL"
    }

    # Attributes
    type = models.CharField(choices=type_choice)
    amount = models.FloatField()
    price = models.FloatField()
    post_date = models.DateTimeField()

