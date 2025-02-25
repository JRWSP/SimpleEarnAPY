import asyncio
from ExchangeClass import CEX
from binance import AsyncClient, Client
from config_secrets import BINANCE_API_KEY, BINANCE_API_SECRET
from typing import Dict

class Binance(CEX):
    def __init__(self, assets = None):
        super().__init__(assets)
        self.api_key:str = BINANCE_API_KEY
        self.api_secret:str = BINANCE_API_SECRET
        self.client = Client(self.api_key, self.api_secret)
        self.SimpleEarnRates:dict = {}

    def _GetCleanResult(self, result:dict) -> dict:
        if result['total']==0:
            print(f"{result['total']=}")
            return result
        earn_data = result['rows'][0]
        asset = earn_data['asset']
        rate_data = {asset: {'latestAnnualPercentageRate': float(earn_data['latestAnnualPercentageRate'])}}
        if 'tierAnnualPercentageRate' in earn_data.keys():
            #If has tier rates.
            tierRate = earn_data['tierAnnualPercentageRate']
            for key, value in tierRate.items():
                # Iterate over the dictionary items and update their values if they are strings
                try:
                    tierRate[key] = float(value) # If successful conversion, replace the original value with a float value
                except ValueError:
                    continue # Value could not be converted to float (e.g., 'abc'), so we keep it as is.
            rate_data[asset]['tierAnnualPercentageRate'] = earn_data['tierAnnualPercentageRate']
        return rate_data
    
    def simpleEarn(self, asset:str) -> dict:
        return self.client.get_simple_earn_flexible_product_list(asset=asset)

    def getSimpleEarnRates(self) -> Dict:
        if self.assets is None:
            print(f"{self.assets=}. Add assets first!")
        else:
            for asset in self.assets:
                result = self._GetCleanResult(self.simpleEarn(asset))
                result = self._formatRate(result)
                self.SimpleEarnRates.update(result)
    
    def _formatRate(self, rate:dict) -> dict:
        asset = [*rate][0]
        rate = rate[asset]
        baseRate = rate['latestAnnualPercentageRate']
        formatRate = []
        if 'tierAnnualPercentageRate' in rate.keys():
            for amt, tierRate in reversed( rate['tierAnnualPercentageRate'].items() ): #Use reversed to show in a correct order.
                formatRate.append({"amt": amt, 
                                'rate': f"{(baseRate+tierRate)*100:.1f}%" })
        formatRate.append({"amt": '', 
                               'rate': f"{baseRate*100:.1f}%" })
        return {asset: formatRate}

class AsyncBinance(Binance):
    """Async Client is no longer used.
    """
    def __init__(self):
        super().__init__()
    
    async def getSimpleEarnRates(self) -> Dict:
        if self.assets is None:
            print(f"{self.assets=}. Add assets first!")
        self.client = await AsyncClient.create(self.api_key, self.api_secret)
        tasks = [self.simpleEarn(asset=asset) for asset in self.assets]
        results = await asyncio.gather(*tasks)
        for result in results:
            self.SimpleEarnRates.update(self._formatRate(self._GetCleanResult(result))) 
        await self.client.close_connection()
