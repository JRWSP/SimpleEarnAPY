# Crypto Simple Earn APR/APY Across CEX.
![prototype version](figure/screenshot%202024-12-18%20011435.png)
-Prototype version on Terminal-

The purpose of this repo is to provide a simple way to monitor the flexible earn yield across well-known CEX.

While cryptocurrencies are risky assets for general audiences, holding stablecoins on time-tested centralized exchanges (CEX) can be a relatively safe way to enjoy high yields. Flexible earn products on those CEX usually offer yields similar or, during a bull market, much higher than T-Bill rates while still preserve the liquidity of the asset. ***Those rates are mostly variable and not guarantee to stay high forever.***

Note that simple earns is not the same as bank's saving account and stablecoins are still a cryptocurrency, they have their own risk that fiat does not. Also please consider this [CEX Transparency list](https://defillama.com/cexs). I suggest you should put any dimes only on a few of top-rank CEXs on the list to minimize counter-party risk. (However, FTX was the 2nd biggest CEX at its golden era so, ***remember, always diversify!.***)  

For those who are risk-taker, there are plenty [defi protocols](https://defillama.com/yields/stablecoins) outside CEX that let you earn yields on stablecoins. Many of them offer higher rates than CEXs but also sports higher risks, please DYOR.

### Supported stablecoin
- USDC
- USDT
## To-do
Some CEX does not provide API for their flexible earn product. I will add them once their API is available.

[ ] Add HTX, Kucion, Gate-io

## Required Pacakge
- python-binance
- python-okx
- bitget sdk (check comments in FetchBitget.py)
- ~~pybit~~ No earning rate API available.

## Setup
1. Getting APIs from CEXs.

## Security Concern

Binance API requires enabling trading permission. This is very risky. If possible, set API with specific ip allowance.


