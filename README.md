# digital-asset-options-pricing
## Table of Contents
- [digital-asset-options-pricing](#digital-asset-options-pricing)
  - [Table of Contents](#table-of-contents)
  - [Motivation](#motivation)
  - [Goals](#goals)
  - [Introduction](#introduction)
    - [Instrument](#instrument)
  - [1 Data Collection and Analysis](#1-data-collection-and-analysis)
  - [X Pricing Models of an Option](#x-pricing-models-of-an-option)
    - [X.X How Realized Volatility affects the pricing models?](#xx-how-realized-volatility-affects-the-pricing-models)
    - [X.X What are some of the pricing models used? What is the IV given the prices](#xx-what-are-some-of-the-pricing-models-used-what-is-the-iv-given-the-prices)
  - [X Option predicted price vs Actual Price comparison](#x-option-predicted-price-vs-actual-price-comparison)
    - [X.X Are the prices / IV compared to the quoted price different?](#xx-are-the-prices--iv-compared-to-the-quoted-price-different)
    - [X.X Is there a model that prices the closest to the quoted price?](#xx-is-there-a-model-that-prices-the-closest-to-the-quoted-price)
    - [Are there any times where the model prices the instrument differently from the quoted prices (outliers)?](#are-there-any-times-where-the-model-prices-the-instrument-differently-from-the-quoted-prices-outliers)
  - [X Possible Trading Strategies](#x-possible-trading-strategies)
  - [Development](#development)
  - [Timeline](#timeline)
  - [Further Exploration](#further-exploration)

## Motivation
Recently, I had an interview for a FX and Rates markets strategy team. During the interview, my biggest difficulty was generating a fair value. I was tasked with generating a Fair Value for a Futures contract, a question I completely fumbled. Next, I was asked to price the cost of a second-hand car. I fumbled that too. The answer was just price of COE * Tax Rebate something along that lines. What I also realized, is that I actually did something like this. I attempted to price an options contract using the Black-Scholes Model, but I stopped because "the problem got too complex" and "nobody uses the Black-Scholes Model". After experiencing this setback, I was so frustrated at myself. These are things that should be at the tips of my fingers! And so, this is my journey on learning to price digital asset options.

## Goals
1. Master the Greeks (Delta, Vega, Theta, Gamma)
   - Understand their definitions and interpretations
   - Analyze their values and market implications
   - Develop trading strategies based on Greek exposures
2. Explore and Enhance Option Pricing Models
   - Study existing models and their assumptions
   - Identify areas for improvement
   - Develop enhanced pricing methodologies
3. Build an Integrated Quantitative Framework
   - Combine financial theory with machine learning (Linear Regression, Tree-based Models)
   - Incorporate time series analysis (ARIMA/GARCH)
   - Create a comprehensive pricing and analysis system
4. Validate Models with Real Market Data
   - Backtest strategies
   - Compare model predictions with actual prices
   - Refine models based on empirical results

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
In this topic, we explore different volatility models, and select the best volatility model to understand digital assets. 

### X.X What are some of the pricing models used? What is the IV given the prices

## X Option predicted price vs Actual Price comparison
This chapter focuses on the estimated price of an option compared to the actual price. 

### X.X Are the prices / IV compared to the quoted price different? 

### X.X Is there a model that prices the closest to the quoted price?

### Are there any times where the model prices the instrument differently from the quoted prices (outliers)?

## X Possible Trading Strategies
This chapter focuses on using the information from the previous chapters to generate a trading strategy that exploits market inefficiencies. Can we use the model to generate a trading strategy based on the mispricing?

Timeframes : 15m, 1h, 24h

---

## Development
- [X] Deribit API Data Collection
- [ ] Pricing
- [ ] Volatility

---

## Timeline

| Week | Tasks | Notes |
|--------------|----------|----------------|
|13 - 19 Jan 25| Organizing Repository, Researching on current projects, Getting inspirations and other ground work. | First week back at NUS! |
|20 - 26 Jan 25| Options, Futures, and Other Derivatives 10th edition, John C. Hull **Chap 14 to 18** <br>  |  |
|27 Jan - 2 Feb 25| **Chap 19-23** | CNY Week, slower progress. |
|3 - 9 Feb 25| Writing Notes. | **Chapter 17-23** |
|10 - 16 Feb 25| Building pricing scripts, testing out different approaches. Observe pricing difference between live and predicted. |  |
|24 Feb - 2 Mar 25| Devise trading strategies, backtest. | |

---

## Further Exploration
- Deribit ETH Options
- Deribit DVOL Futures
- Binance BTC/ETH Options
- CCXT Integration - https://github.com/ccxt/ccxt/wiki/Manual