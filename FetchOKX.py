from okx import Earning
from config_secrets import OKX_API_KEY, OKX_API_PASSPHRASE, OKX_API_SECRET

###Sequential version
class OKX():
    def __init__(self):
        self.API = Earning.EarningAPI(OKX_API_KEY, OKX_API_SECRET, OKX_API_PASSPHRASE, 
                                      use_server_time=False, flag='0', debug=False, proxy=None)
    def onchainEarn(self, asset:str) -> dict:
        return self.API.get_offers(ccy=asset)

    def simpleEarn(self, asset:str) -> dict:
        return self.API.get_public_borrow_info(ccy=asset)