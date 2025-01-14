# digital-asset-options-pricing

## Motivation
Recently, I had an interview for a FX and Rates markets strategy team. During the interview, my biggest difficulty was generating a fair value. I was tasked with generating a Fair Value for a Futures contract, a question I completely fumbled. Next, I was asked to price the cost of a second-hand car. I fumbled that too. The answer was just price of COE * Tax Rebate something along that lines. What I also realized, is that I actually did something like this. I attempted to price an options contract using the Black-Scholes Model, but I stopped because "the problem got too complex" and "nobody uses the Black-Scholes Model". After experiencing this setback, I was so frustrated at myself. These are things that should be at the tips of my fingers! And so, this is my journey on learning to price digital asset options.

## Goals
1. Understanding the Greeks - Delta, Vega, Theta, Gamma. Definitions, values, and what are the implications of the values. Maybe, also how to trade the greeks.
2. Understand Option Pricing Models - and how to make them better.
3. Doing a project that combines both Finance + ML (Linear Regression / Tree-based Models) + Time Series (ARIMA/GARCH)
4. 

## Introduction
The goal of this repository is to identify mispricing of digital asset options. In digital assets, retail has easy access to leverage through Perpetual contracts, which are much easier to understand and execute. As a result, the current options market (080125) is dominated by a few institutional players. My hypothesis is that the market is still highly inefficient given this understanding. In this repository, I will develop scripts to collect the data, run an analysis, develop multiple pricing models, and then develop trading strategies to arbitrage the mispricing of an option. 

### Instrument
The main instrument of focus will be the Deribit BTC Options (Weeklies, Monthlies, Quarterlies).

Key Notes:
- European Options
- Expirations always take place at 08:00 UTC, on Friday.
- Time-weighted average of Deribit BTC index, as measured between 07:30 and 08:00 UTC.
- Fees
  - Maker: 0.0001 * index price
  - Taker: 0.0005 * index price
  - Settlement: 0.00015 * index price

For more information, refer to the [knowledge base](https://www.deribit.com/kb/linear_usdc_options) and the [introduction policy](https://www.deribit.com/kb/deribit-introduction-policy)

## 1 Data Collection and Analysis
This chapter focuses on the development of a data collection module for Deribit Options.

## X Pricing Models of an Option
This chapter focuses on the development of multiple pricing models for an European Option. In this chapter, we will design multiple models with different approaches to calculate the price of an European Option.

### X.X How Realized Volatility affects the pricing models? 

### X.X What is the IV given the prices?

## X Option predicted price vs Actual Price comparison
This chapter focuses on the estimated price of an option compared to the actual price. 

### X.X How different are the prices / IV compared to the quoted price?

### X.X Which is better? Model or Actual? Is there a better way to price?

## X Possible Trading Strategies
This chapter focuses on using the information from the previous chapters to generate a trading strategy that exploits market inefficiencies. 

Timeframes : 15m, 1h, 24h

## Further Exploration

- Deribit ETH Options
- Deribit DVOL Futures
- Binance BTC/ETH Options

## Development

## References

### Books

### X

### Papers