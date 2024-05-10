from django.contrib import admin

# Register your models here.
from crypto_dash.models import (Exchanges, Symbols,)

@admin.register(Exchanges)
class ExchangesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    class Meta:
        ordering = ("id", "name")

@admin.register(Symbols)
class Symbols(admin.ModelAdmin):
    list_display = ("id", "name")
    
    class Meta:
        ordering = ("id", "name")
    