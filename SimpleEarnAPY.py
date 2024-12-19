from config_secrets import *
from FetchBybit import Bybit
from FetchBitget import Bitget
from FetchOKX import OKX
from FetchKucoin import Kucoin
from FetchBinance import Binance
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time 

def fetch_and_return_rates(ExchangeClass: classmethod, assets: str|list) -> tuple[str,dict]:
    exchange = ExchangeClass(assets=assets)
    exchange.getSimpleEarnRates()
    print(f"Finish fetching {ExchangeClass.__name__}")
    return (ExchangeClass.__name__ , exchange.SimpleEarnRates)

def formatDataFrame(cex:str, EarnRates:dict) -> pd.DataFrame:
    ratesDF = None
    for coin, rates in EarnRates.items():
        df = pd.DataFrame.from_dict(rates)
        df['coin'] = [coin]*len(df)
        df['cex'] = [cex]*len(df)
        df = df[['cex','coin','rate','amt']]
        ratesDF = pd.concat([ratesDF, df], ignore_index=True)
    return ratesDF

def main():
    assets = ['USDC','USDT']
    exchanges = [
        Binance,
        Bitget,
        OKX,
        Kucoin,
        Bybit
    ]
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_and_return_rates, cls, assets) for cls in exchanges]    
    results = [future.result() for future in futures]

    rateDataFrame = [formatDataFrame(cex, result) for (cex, result) in results]
    rateDataFrame = pd.concat(rateDataFrame, ignore_index=True)
    return rateDataFrame.to_string(index=False)

if __name__=="__main__":
    start_time = time.time()
    print(main())
    multithreaded_duration = time.time() - start_time
    print(f"Multithreaded execution took {multithreaded_duration:.2f} seconds.\n")