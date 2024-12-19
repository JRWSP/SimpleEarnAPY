# Crypto Simple Earn APR/APY Across CEX.
If you find my project helpful, you can donate me for a cup of coffee, or some beers so I can code more :) <br>

<a href="https://www.buymeacoffee.com/jrwsp" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 108px !important;" ></a> <br>
BTC: bc1q2zpmmlz7ujwx2ghsgw5j7umv8wmpchplemvhtu <br>
ETH: 0x80e98FcfED62970e35a57d2F1fefed7C89d5DaF4
![prototype version](figure/screenshot%202024-12-18%20011435.png)

The purpose of this repo is to provide a simple way to monitor the flexible earn yield across well-known CEX.

While cryptocurrencies are risky assets for general audiences, holding stablecoins on time-tested centralized exchanges (CEX) can be a relatively safe way to enjoy high yields. Flexible earn products on those CEX usually offer yields similar or, during a bull market, much higher than T-Bill rates while still preserve the liquidity of the asset. ***Those rates are mostly variable and not guarantee to stay high forever.***

Note that simple earns is not the same as bank's saving account and stablecoins are still a cryptocurrency, they have their own risk that fiat does not. Also please consider this [CEX Transparency list](https://defillama.com/cexs). I suggest you should put any dimes only on a few of top-rank CEXs on the list to minimize counter-party risk. (However, FTX was the 2nd biggest CEX at its golden era so, ***remember, always diversify!.***)  

For those who are risk-taker, there are plenty [defi protocols](https://defillama.com/yields/stablecoins) outside CEX that let you earn yields on stablecoins. Many of them offer higher rates than CEXs but also sports higher risks, please DYOR.

### Supported stablecoin
USDC, USDT
### Supported CEX
Binance, OKX, Bitget, Kucoin, Bybit


### Unsupported CEX
Some CEX does not provide API for their flexible earn product. I will add them once their API is available.

HTX, Crypto.com, Coinbase, Gate-io

## To-do

## Required Pacakge
- python-binance
- python-okx
- bitget sdk (check comments in FetchBitget.py)
- kucoin-universal-sdk
- pandas

## How to use
1. Download or clone this repo.
2. Install the required packages by go to your downloaded folder and run
```sh
pip install -r requirements.txt
``` 
3. Getting APIs from CEXs. Create `config_secrets.py` file to store your API keys. These keys are very important, always keep it safe from the others. The file should looks like this:
```python
# Binance API credentials
BINANCE_API_KEY = 'xxx'
BINANCE_API_SECRET = 'xxx'

#OKX API credentials
OKX_API_KEY = 'xxx'
OKX_API_SECRET = 'xxx'
OKX_API_PASSPHRASE = 'xxx'

#Bitget API credentials
BITGET_API_KEY = 'xxx'
BITGET_API_SECRET = 'xxx'
BITGET_API_PASSPHRASE = 'xxx'

#Kucoin API credentials
KUCOIN_API_KEY = 'xxx'
KUCOIN_API_SECRET = 'xxx'
KUCOIN_API_PASSPHRASE = 'xxx'
```
4. Finally, run:
```sh
python SimpleEarnAPY.py
```
## Security Concern

- Bybit fetching uses selenium, which is very less efficient than the API metohd. If you do not care about this exchange, turn it off will make program run much faster. This can be done by remove `Bybit` from `exchange` variable in the main file.
- Binance API requires enabling trading permission. This is very risky. If possible, set API with specific ip allowance.


