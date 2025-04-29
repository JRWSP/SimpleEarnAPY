import okx.Finance.Savings as Savings
from ExchangeClass import CEX
from config_secrets import OKX_API_KEY, OKX_API_PASSPHRASE, OKX_API_SECRET

###Sequential version
class OKX(CEX):
    def __init__(self, assets = None):
        super().__init__(assets)
        #self.api_key:str = OKX_API_KEY
        #self.api_secret:str = OKX_API_SECRET
        #self.api_passphrase = OKX_API_PASSPHRASE
        flag = "0"  # Production trading:0 , demo trading:1
        self.API = Savings.SavingsAPI(flag=flag)
        #self.API = Earning.EarningAPI(self.api_key, self.api_secret, self.api_passphrase, 
        #                              use_server_time=False, flag='0', debug=False, proxy=None)
        self.SimpleEarnRates:dict = {}

    def onchainEarn(self, asset:str) -> dict:
        return self.API.get_offers(ccy=asset)

    def simpleEarn(self, asset:str) -> dict:
        return self.API.get_public_borrow_info(ccy=asset)

    def _formatRate(self, rate:dict) -> dict:
        return { rate['ccy']:[{'amt': '',
                               'rate': f"{float(rate['estRate'])*100:.1f}%"}] }

    def getSimpleEarnRates(self):
        if self.assets is None:
            print(f"{self.assets=}. Add assets first!")
        else:
            for asset in self.assets:
                try:
                    rate = self.simpleEarn(asset)
                    rate = rate['data'][0]
                    self.SimpleEarnRates.update(self._formatRate(rate))
                except Exception as e:
                    print(e)
                    continue