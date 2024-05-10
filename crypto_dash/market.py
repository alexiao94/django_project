from coinapi_rest_v1.restapi import CoinAPIv1
from crypto_dash.models import (Records,Symbols,Exchanges,Fiat,Type)
from pprint import pprint
from datetime import datetime

class market():
    def __init__(self) -> None:
        self.market_key = "56ACE695-1A35-4B3B-8921-1F3BC56DBED5"
        self.api = CoinAPIv1(self.market_key)
        
    def lookup(self, exchange:str, type:str, coin:str, fiat:str, time:str) -> None:
        symbol_id = "_".join([exchange, type, coin, fiat])
        ohlcv_historical = self.api.ohlcv_historical_data(symbol_id, {'period_id': time, 'limit':100000})
        for period in ohlcv_historical:
            print('Period start: %s' % period['time_period_start'])
            print('Period end: %s' % period['time_period_end'])
            print('Time open: %s' % period['time_open'])
            print('Time close: %s' % period['time_close'])
            print('Price open: %s' % period['price_open'])
            print('Price close: %s' % period['price_close'])
            print('Price low: %s' % period['price_low'])
            print('Price high: %s' % period['price_high'])
            print('Volume traded: %s' % period['volume_traded'])
            print('Trades count: %s' % period['trades_count'])

    def record_data(self, exchange:str, type:str, coin:str, fiat:str, time:str) -> None:
        symbol_id = "_".join([exchange.name, type.name, coin.id, fiat.id])
        ohlcv_historical = self.api.ohlcv_historical_data(symbol_id, {'period_id': time, 'limit':100000})
        _symbol = Symbols.objects.get(id=coin.id) 
        _exchange = Exchanges.objects.get(id=exchange.id)
        _fiat = Fiat.objects.get(id=fiat.id)
        _type = Type.objects.get(id=type.id)

        for period in ohlcv_historical:
            record = Records(symbol=_symbol,
                             exchange=_exchange,
                             fiat=_fiat,
                             type=_type,
                             price_open=float(period['price_open']),
                             price_close = float(period['price_close']),         
                             price_low = float(period['price_low']),
                             price_high = float(period['price_high']),
                             time_open = period['time_open'],
                             time_close = period['time_close'],)
            record.save()


      
# market().lookup(exchange="COINBASE",type="SPOT",coin="BTC",fiat="USD",time='1HRS')
