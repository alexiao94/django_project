from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Symbols(models.Model):
    # Primary key
    id = models.CharField(primary_key=True, max_length=20)

    # Attributes
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.id}, {self.name}"
    
class Fiat(models.Model):
    # Primary key
    id = models.CharField(primary_key=True, max_length=20)

    # Attributes
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.id}, {self.name}"
    
class Exchanges(models.Model):
    # Primary key
    id = models.CharField(primary_key=True, max_length=20)

    # Attributes
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.id}, {self.name}"
    
class Type(models.Model):
    # Primary key
    id = models.CharField(primary_key=True, max_length=20)

    # Attributes
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.id}, {self.name}"
    
class Time(models.Model):
    # Primary key
    id = models.CharField(primary_key=True, max_length=20)

    # Attributes
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.id}, {self.name}"
    
class Records(models.Model):
    # Primary key
    id = models.AutoField(primary_key=True)

    # Foreign keys
    symbol = models.ForeignKey(Symbols, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchanges, on_delete=models.CASCADE)
    fiat = models.ForeignKey(Fiat,on_delete=models.CASCADE)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    
    # Attributes
    price_open = models.FloatField()
    price_close = models.FloatField()
    price_low = models.FloatField()
    price_high = models.FloatField()
    time_open = models.DateTimeField()
    time_close = models.DateTimeField()
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    volume = models.FloatField()
    trades = models.FloatField()

class Transactions(models.Model):
    # Primary key
    id = models.AutoField(primary_key=True)

    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbols, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchanges, on_delete=models.CASCADE)

    type_choice = (
        ('B', "BUY"),
        ('S', "SELL"),
    )

    # Attributes
    type = models.CharField(choices=type_choice, max_length=20)
    amount = models.FloatField()
    price = models.FloatField()
    post_date = models.DateTimeField()

