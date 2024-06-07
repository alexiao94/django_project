from coinapi_rest_v1.restapi import CoinAPIv1
from crypto_dash.models import (Records,Symbols,Exchanges,Fiat,Type,Time)
from pprint import pprint
from datetime import datetime
from tqdm import tqdm
from websocket import create_connection
import json
import os  
import time
class market():
    def __init__(self) -> None:
        self.market_key = os.getenv("MARKET_API_KEY")
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
        _symbol = Symbols.objects.get(id=coin.id) 
        _exchange = Exchanges.objects.get(id=exchange.id)
        _fiat = Fiat.objects.get(id=fiat.id)
        _type = Type.objects.get(id=type.id)
        _time = Time.objects.get(id=time.id)
        last_record = Records.objects.filter(time=_time).last()

        if last_record:
            print("Found records...")
            last_time_start = last_record.time_open.replace(microsecond=0).isoformat()
            ohlcv_historical = self.api.ohlcv_historical_data(symbol_id, {'time_start':last_time_start,'period_id': _time.id, 'limit':100})
            ohlcv_historical.reverse()
            ohlcv_historical_last_open = datetime.fromisoformat(ohlcv_historical[-1]['time_open']).replace(microsecond=0)
      
            if  (ohlcv_historical_last_open == last_record.time_open.replace(microsecond=0)):
                print("Updating last entry...")
                last_record.price_close = float(ohlcv_historical[-1]['price_close'])
                last_record.price_low = float(ohlcv_historical[-1]['price_low'])
                last_record.price_high = float(ohlcv_historical[-1]['price_high'])
                last_record.time_close = float(ohlcv_historical[-1]['time_close'])
                last_record.volume = float(ohlcv_historical[-1]["volume_traded"])
                last_record.trades = float(ohlcv_historical[-1]["trades_count"])
                last_record.save()
            else:
                # record_list = []
                print("Found a total of", len(ohlcv_historical), "records to add...")
                for i in  tqdm (range(len(ohlcv_historical)), desc="Loading..."):
                    period = ohlcv_historical[i]
                    record = Records(symbol=_symbol,
                                    exchange=_exchange,
                                    fiat=_fiat,
                                    type=_type,
                                    time=_time,
                                    price_open=float(period['price_open']),
                                    price_close = float(period['price_close']),         
                                    price_low = float(period['price_low']),
                                    price_high = float(period['price_high']),
                                    time_open = period['time_open'],
                                    time_close = period['time_close'],
                                    period_start = period["time_period_start"],
                                    period_end = period["time_period_end"],
                                    volume = float(period["volume_traded"]),
                                    trades = float(period["trades_count"]))
                    record.save()
                    # record_list.append(record)
                # new_records = Records.objects.bulk_create(record_list)
        else:
            print("No records available")
            ohlcv_historical = self.api.ohlcv_historical_data(symbol_id, {'period_id': _time.id, 'limit':100})
            ohlcv_historical.reverse()
            # record_list = []
            print("Found a total of", len(ohlcv_historical), "records to add")
            for i in  tqdm (range(len(ohlcv_historical)), desc="Loading..."):
                period = ohlcv_historical[i]
                record = Records(symbol=_symbol,
                                exchange=_exchange,
                                fiat=_fiat,
                                type=_type,
                                time=_time,
                                price_open=float(period['price_open']),
                                price_close = float(period['price_close']),         
                                price_low = float(period['price_low']),
                                price_high = float(period['price_high']),
                                time_open = period['time_open'],
                                time_close = period['time_close'],
                                period_start = period["time_period_start"],
                                period_end = period["time_period_end"],
                                volume = float(period["volume_traded"]),
                                trades = float(period["trades_count"]))
                record.save()
            # new_records = Records.objects.bulk_create(record_list)
            

    def stream_record(self, exchange:str, type:str, coin:str, fiat:str, time:str): 

        _symbol = Symbols.objects.get(id=coin.id) 
        _exchange = Exchanges.objects.get(id=exchange.id)
        _fiat = Fiat.objects.get(id=fiat.id)
        _type = Type.objects.get(id=type.id)
        _time = Time.objects.get(id=time.id)
        ws = create_connection("wss://ws.coinapi.io/v1")
        subs = {"type":"subscribe", 
                "apikey":self.market_key,
                "hearbeat":True,
                "subscribe_data_type": ["ohlcv"],
                "subscribe_filter_asset_id":[_symbol.name+'/'+_fiat.name],
                "subscribe_filter_exchange_id":[_exchange.name],
                "subscribe_filter_period_id":[_time.id]
                }
        ws.send(json.dumps(subs))

        last_record = Records.objects.filter(time=_time).last()
        last_period_start = last_record.period_end
        api_last_period_start = ws.recv()["time_period_start"]

        if api_last_period_start != last_period_start:
            self.record_data(exchange,type,coin,fiat,time)
            last_period_start = api_last_period_start

        while True:
            msg = ws.recv()
            period_start = msg["time_period_start"]
            period_end = msg["time_period_end"]
            time_open = msg["time_open"]
            time_close = msg["time_close"]
            price_open = msg["price_open"]
            price_high = msg["price_high"]
            price_low = msg["price_low"]
            price_close = msg["price_close"]
            volume = msg["volume_traded"]
            trades = msg["trades_count"]

            if last_period_start != period_start:
                record = Records(symbol=_symbol,
                            exchange=_exchange,
                            fiat=_fiat,
                            type=_type,
                            time=_time,
                            price_open=float(price_open),
                            price_close = float(price_close),         
                            price_low = float(price_low),
                            price_high = float(price_high),
                            time_open = time_open,
                            time_close = time_close,
                            period_start = period_start,
                            period_end = period_end,
                            volume = float(volume),
                            trades = float(trades)
                )
                record.save()
                last_period_start = period_start
            else:
                yield msg
            time.sleep(5)

# market().record_data('COINBASE','SPOT','BTC','USD','1HRS')
      
# market().lookup(exchange="COINBASE",type="SPOT",coin="BTC",fiat="USD",time='1HRS')

# market().stream_record(exchange="COINBASE",type="SPOT",coin="BTC",fiat="USD",time='1HRS')