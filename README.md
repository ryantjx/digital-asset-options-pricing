# Deribit Options Pricing and Theoretical Value
## Table of Contents
<!-- - [Deribit Options Pricing and Theoretical Value](#deribit-options-pricing-and-theoretical-value)
  - [Table of Contents](#table-of-contents) -->
- [Deribit Options Pricing and Theoretical Value](#deribit-options-pricing-and-theoretical-value)
  - [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
  - [Motivation](#motivation)
  - [Goals](#goals)
  - [Instrument](#instrument)
- [Development Timeline](#development-timeline)
  - [Progress](#progress)
  - [Schedule](#schedule)
  - [Milestones](#milestones)
- [Further Exploration](#further-exploration)

# Introduction
The goal of this repository is to identify mispricing of digital asset options. In digital assets, retail has easy access to leverage through Perpetual contracts, which are much easier to understand and execute. As a result, the current options market (080125) is dominated by a few institutional players. My hypothesis is that the market is still highly inefficient given this understanding. In this repository, I will develop scripts to collect the data, run an analysis, develop multiple pricing models, and then develop trading strategies to arbitrage the mispricing of an option. 

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

## Instrument
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

Timeframes : 15m, 1h, 24h

---

# Development Timeline

## Progress
- [X] Deribit API Data Collection
- [ ] Pricing
- [ ] Market Prices vs Model-Derived theoretical values.
- [ ] Volatility
- [ ] Sensitivity Analysis 

## Schedule

| Week | Tasks | Notes |
|--------------|----------|----------------|
|13 - 19 Jan 25| Organizing Repository, Researching on current projects, Getting inspirations and other ground work. | First week back at NUS! |
|20 - 26 Jan 25| Options, Futures, and Other Derivatives 10th edition, John C. Hull **Chap 14 to 18** <br>  |  |
|27 Jan - 2 Feb 25| **Chap 19-23** | CNY Week, slower progress. |
|3 - 9 Feb 25| Writing Notes. | **Chapter 17-23** | 
|10 - 16 Feb 25| Completing Notes | **Chapter 20-23** |
|17 - 23 Feb 25| Brainstorming, build pricing scripts, compare pricing difference. |  |
|24 Feb - 2 Mar 25| Devise trading strategies, backtest. | |

## Milestones

--- 
# Further Exploration
- Instruments
  - Deribit ETH Options
  - Deribit DVOL Futures
  - Binance BTC/ETH Options
  - CCXT Integration - https://github.com/ccxt/ccxt/wiki/Manual
- Options Tools
  - GV (Graph Vol) - This is a powerful visualization tool for options volatility. It allows you to plot implied volatility surfaces and term structures, helping traders understand how volatility varies across different strike prices and expiration dates.
  - HVG (Historical Volatility Graph) - This shows historical volatility patterns over time. It's crucial for comparing current implied volatility levels against historical realized volatility, which helps in determining if options are relatively expensive or cheap.
  - VCA (Volatility/Correlation Analysis) - Analyzes relationships between volatilities of different instruments and their correlations, particularly useful for multi-asset options strategies.
- Pricing Exotic Options