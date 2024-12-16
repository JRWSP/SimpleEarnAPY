import time
from pprint import pprint
import asyncio
from FetchBinance import *
from config_secrets import *

if __name__=="__main__":
    assets = ['USDC','USDT']

    start = time.time()
    loop = asyncio.get_event_loop()
    rates = loop.run_until_complete(async_fetch_on_binance(assets))
    end = time.time()
    async_time = end - start
    pprint(rates)
    print(f"{async_time=}")