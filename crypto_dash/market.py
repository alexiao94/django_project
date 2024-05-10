from coinapi_rest_v1.restapi import CoinAPIv1
from pprint import pprint
import datetime

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

    # for i in api.metadata_list_exchanges():   
    #     print(i['website'], i['exchange_id'])
    # ohlcv_historical = api.ohlcv_historical_data('COINBASE_SPOT_SHIB_USD', {'period_id': '1HRS', 'limit':100000})
    # print(len(ohlcv_historical))

# for period in ohlcv_historical:
#     print('Period start: %s' % period['time_period_start'])
#     print('Period end: %s' % period['time_period_end'])
#     print('Time open: %s' % period['time_open'])
#     print('Time close: %s' % period['time_close'])
#     print('Price open: %s' % period['price_open'])
#     print('Price close: %s' % period['price_close'])
#     print('Price low: %s' % period['price_low'])
#     print('Price high: %s' % period['price_high'])
#     print('Volume traded: %s' % period['volume_traded'])
#     print('Trades count: %s' % period['trades_count'])
