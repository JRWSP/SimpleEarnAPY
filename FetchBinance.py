import nest_asyncio
nest_asyncio.apply()
import asyncio
from binance import AsyncClient
from config_secrets import BINANCE_API_KEY, BINANCE_API_SECRET
from typing import List, Dict

async def async_fetch_on_binance(assets:str|List[str]) -> Dict:
    if isinstance(assets, str):
        assets = [assets]
    # initialise the client
    binance_rates = {}
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    tasks = [client.get_simple_earn_flexible_product_list(asset=asset) for asset in assets]
    results = await asyncio.gather(*tasks)
    for result in results:
        if result['total']==0:
            continue
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
        binance_rates.update(rate_data) 
    await client.close_connection()
    return binance_rates