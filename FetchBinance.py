import requests
import aiohttp
import time
import hmac
import hashlib
from typing import List, Dict, Optional
import asyncio
from config_secrets import *

###Sequential version
def binance_simple_earn_flexible(asset:str) -> Optional[dict]:
    BASE_URL = 'https://api.binance.com'
    endpoint = '/sapi/v1/simple-earn/flexible/list'
    params = {
        'asset': asset,
        'timestamp': int(time.time() * 1000 - 1000),  # Current timestamp in milliseconds
    }
    
    # Create the signature
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(
        BINANCE_API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Add the signature to the parameters
    params['signature'] = signature

    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }
    
    # Send the request
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        # Success
        data = response.json()
        return data['rows'][0]
    else:
        # Error
        print(f"Error: {response.status_code}, {response.text}")
        return None

def fetch_on_binance(assets:str|List[str]) -> Dict:
    """Fetch assets' simple earn rates on Binance.

    Args:
        assets (str | List[str]): Name(s) of asset(s).

    Returns:
        Dict: 
    """
    binance_rates = {}
    assets = [assets] if isinstance(assets,str) else assets
    for asset in assets:
        earn_data = binance_simple_earn_flexible(asset)
        if earn_data is None:
            continue #skip the asset if cannot find on Binance.
        rate_data = {earn_data['asset']: {'latestAnnualPercentageRate': float(earn_data['latestAnnualPercentageRate'])}}
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
    return binance_rates

###Async version
async def async_binance_simple_earn_flexible(asset:str) -> Optional[dict]:
    BASE_URL = 'https://api.binance.com'
    endpoint = '/sapi/v1/simple-earn/flexible/list'
    params = {
        'asset': asset,
        'timestamp': int(time.time() * 1000 - 1000),  # Current timestamp in milliseconds
    }
    
    # Create the signature
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(
        BINANCE_API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Add the signature to the parameters
    params['signature'] = signature

    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }
    # Use aiohttp for the async request
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + endpoint, headers=headers, params=params) as response:
            if response.status == 200:
                # Success
                data = await response.json()
                return data['rows'][0] if 'rows' in data and data['rows'] else None
            else:
                # Error
                print(f"Error: {response.status}, {await response.text()}")
                return None   

async def async_fetch_on_binance(assets:str|List[str]) -> Dict:
    """Fetch assets' simple earn rates on Binance.

    Args:
        assets (str | List[str]): Name(s) of asset(s).

    Returns:
        Dict: 
    """
    binance_rates = {}
    assets = [assets] if isinstance(assets,str) else assets
    tasks = [async_binance_simple_earn_flexible(asset) for asset in assets]
    results = await asyncio.gather(*tasks)
    for earn_data in results:
        if earn_data is None:
            continue #skip the asset if cannot find on Binance.
        asset = earn_data['asset']
        rate_data = {earn_data['asset']: {'latestAnnualPercentageRate': float(earn_data['latestAnnualPercentageRate'])}}
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
    return binance_rates