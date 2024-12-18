from ExchangeClass import CEX
from config_secrets import KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE
from kucoin_universal_sdk.api.client import DefaultClient
from kucoin_universal_sdk.model.client_option import ClientOptionBuilder
from kucoin_universal_sdk.model.constants import GLOBAL_API_ENDPOINT
from kucoin_universal_sdk.model.transport_option import TransportOptionBuilder
from kucoin_universal_sdk.generate.earn.earn.model_get_staking_products_req import GetStakingProductsReq

class Kucoin(CEX):
    def __init__(self, assets = None):
        super().__init__(assets)
        self.api_key = KUCOIN_API_KEY
        self.api_secret = KUCOIN_API_SECRET
        self.api_passphrase = KUCOIN_API_PASSPHRASE
        # Set specific options, others will fall back to default values
        http_transport_option = (
            TransportOptionBuilder()
            .build()
        )
        # Create a client using the specified options
        client_option = (
            ClientOptionBuilder()
            .set_key(self.api_key)
            .set_secret(self.api_secret)
            .set_passphrase(self.api_passphrase)
            .set_spot_endpoint(GLOBAL_API_ENDPOINT)
            .set_transport_option(http_transport_option)
            .build()
        )
        client = DefaultClient(client_option)
        # Get the Restful Service
        self.kucoin_rest_service = client.rest_service()
        self.earn = self.kucoin_rest_service.get_earn_service()
    
    def simpleEarn(self, asset:str) -> dict:
        req=GetStakingProductsReq(currency=asset)
        rate = self.earn.earn.get_savings_products(req=req)
        rate = rate.model_dump()
        rate = rate['data'][0]['return_rate']
        rate = f"{float(rate)*100:.1f}%"
        return {asset: [{'amt':'', 'rate':rate}]}
    
    def getSimpleEarnRates(self):
        if self.assets is None:
            print(f"{self.assets=}. Add assets first!")
        else:
            for asset in self.assets:
                result = self.simpleEarn(asset)
                self.SimpleEarnRates.update(result)