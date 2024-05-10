from django.contrib import admin
from crypto_dash.models import (Exchanges, Symbols, Fiat,Records,Type,)
from crypto_dash.market import market
from django.utils import timezone

@admin.register(Exchanges)
class ExchangesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    class Meta:
        ordering = ("id", "name")

@admin.register(Symbols)
class SymbolsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    
    class Meta:
        ordering = ("id", "name")

@admin.register(Fiat)
class FiatsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    
    class Meta:
        ordering = ("id", "name")

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    
    class Meta:
        ordering = ("id", "name")

@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):

    exclude = ('price_open','price_close', 'price_low', 'price_high','time_open','time_close')
    list_display = ("id", "symbol", "exchange", "fiat", "type", 'price_open','price_close', 'price_low', 'price_high','time_open','time_close')
    ordering = ["-time_close"]
        
    def save_model(self, request, obj, form, change):
        #super().save_model(request, obj, form, change)

        exchange = obj.exchange
        type = obj.type
        coin = obj.symbol
        fiat = obj.fiat
       
        market().record_data(exchange=exchange,type=type,coin=coin,fiat=fiat,time='1HRS')


