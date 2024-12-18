"""
If you clone this project directly from my Github repo, the 'bitget' is already included and the step below is unnecessary.

Bitget does not provide sdk though pip channel. 
You need to download it from their github repo (https://github.com/BitgetLimited/v3-bitget-api-sdk/tree/master/bitget-python-sdk-api) 
and put the folder 'bitget' from v3-bitget-api-sdk/bitget-python-sdk-api to your local directory.

Parameter	Type	Required	Description
coin	    String	No	Coin eg： BTC
filter	    String	No	Filter conditions
                        available Available for subscription
                        held Held
                        available_and_held Available for subscription and held
                        all Query all Including those that have been removed from the shelves
"""
from ExchangeClass import CEX
from config_secrets import BITGET_API_KEY, BITGET_API_SECRET, BITGET_API_PASSPHRASE
import bitget.bitget_api as baseApi
from bitget.exceptions import BitgetAPIException

class Bitget(CEX):
    def __init__(self, assets = None):
        super().__init__(assets)
        self.api_key:str = BITGET_API_KEY
        self.api_secret:str = BITGET_API_SECRET
        self.api_passphrase = BITGET_API_PASSPHRASE
        self.endpoint = "/api/v2/earn/savings/product"
        self.baseApi = baseApi.BitgetApi(self.api_key, self.api_secret, self.api_passphrase)

    def simpleEarn(self, asset:str) -> list:
        try:
            response = self.baseApi.get(self.endpoint, params={"coin":asset})
            return response['data'][0]['apyList'] #0 for flexible, 1 for fixed.
        except BitgetAPIException as e:
            print("error:" + e.message)

    def _formatRate(self, rate:dict) -> list:
        formatRate = []
        for tier in rate:
            amt = f"{int(float(tier['minStepVal'])):,}-{int(float(tier['maxStepVal'])):,}"
            rate = f"{float(tier['currentApy']):.1f}%"
            formatRate.append({'amt':amt,
                               'rate':rate})
        return formatRate

    def getSimpleEarnRates(self):
        if self.assets is None:
            print(f"{self.assets=}. Add assets first!")
        else:
            for asset in self.assets:
                rate = self.simpleEarn(asset)
                self.SimpleEarnRates.update({asset: self._formatRate(rate)})