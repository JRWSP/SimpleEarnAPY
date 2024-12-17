from typing import List
class CEX:
    def __init__(self):
        self.api_key:str = None
        self.api_secret:str = None
        self.api_passphrase = None
        self.assets:list = None 
        self.SimpleEarnRates:dict = {}

    def addAssets(self, assets:str|List[str]) -> None:
        if isinstance(assets, str):
            assets = [assets]
        self.assets = assets

    def simpleEarn(self, asset:str) -> dict:
        pass

    def getSimpleEarnRates(self) -> dict:
        pass

    def _formatRate(self) -> dict:
        pass