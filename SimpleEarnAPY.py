from pprint import pprint
from config_secrets import *
from FetchBitget import Bitget
from FetchOKX import OKX
from FetchBinance import AsyncBinance, Binance
if __name__=="__main__":
    assets = ['USDC','USDT']
    print("Binance")
    if len(assets) > 2:
#        import nest_asyncio
#        nest_asyncio.apply()
        import asyncio

        binance = AsyncBinance()
        binance.addAssets(assets)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(binance.getSimpleEarnRates())
    else:
        binance = Binance()
        binance.addAssets(assets)
        binance.getSimpleEarnRates()

    pprint(binance.SimpleEarnRates)

    print("Bitget")
    bitget = Bitget()
    bitget.addAssets(assets)
    bitget.getSimpleEarnRates()
    pprint(bitget.SimpleEarnRates)

    print("OKX")
    okx = OKX()
    okx.addAssets(assets)
    okx.getSimpleEarnRates()
    pprint(okx.SimpleEarnRates)