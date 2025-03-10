## References

### Books
1. Options, Futures, and Other Derivatives 10th edition, John C. Hull
2. Option Volatility and Pricing: Advanced Trading Strategies and Techniques (2ND), Sheldon Natenberg
3. Stochastic Volatility Modeling, Lorenzo Bergomi 

### Papers
#### Pricing
1. [Bakshi, G., C. Cao, and Z. Chen. “Empirical Performance of Alternative Option Pricing Models,” Journal of Finance, 52, No. 5 (December 1997): 2004–49.](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1997.tb02749.x)
   1. Alternative Models
      1. (i) the Black-Scholes (BS) model, 
      2. (ii) the stochastic-interest-rate (SI) model, 
      3. (iii) the stochastic-volatility (SV) model, 
      4. (iv) the stochastic-volatility and stochastic-interest-rate (SVSI) model, and 
      5. (v) the stochastic-volatility random-jump (SVJ) model
   2. Evaluation
      1. internal consistency of implied parameters/volatility with relevant time-series data
      2. out-of-sample pricing
      3. hedging
2. [Options Driven Volatility Forecasting](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4790644)
   1. some inspiration for further improvements - utilizing volatility forecasting to help in pricing. Use a regression model to get to improve pricing with other factors.
#### Strategies
1. ["Which Free Lunch Would You Like Today, Sir?: Delta Hedging, Volatility Arbitrage and Optimal Portfolios](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=22554822cff90a56962f8ce4327587e86a42f1dc)
    - How to profit when there's a difference between the market's implied volatility (used in option pricing) and the actual volatility of the underlying asset. Hedging options mispriced by the market.
    - Which delta do you choose? Delta based on RV or IV? 
    - Black Scholes: $d_1 = \frac{\ln\left(\frac{S}{E}\right) + \left(r + \frac{1}{2}\sigma^2\right)(T-t)}{\sigma\sqrt{T-t}}$
    - Case 1: Hedging with Actual Volatility
      - Provides a guaranteed profit equal to the difference between option values using actual vs implied volatility
    - Case 2: Hedging with IV (Chosen for Optimization)
        - By hedging with implied volatility we are balancing the random fluctuations in the mark-to-market option value with the fluctuations in the stock price.
    - 10.1 Dynamics linked via drift rates
      - Profit depends crucially on the growth rate because of the path dependence.
      - $dS_i = μ_i(S1,..., Sn) dt + σ_iS_i dX_i$
    - Extra Notes
      - Mark-to-Market vs Mark-to-Model
        - Mark-to-market refers to valuing assets based on current market prices - what you could actually buy or sell them for right now.
        - Mark-to-model involves valuing assets using theoretical pricing models, like Black-Scholes for options. 
    - References
      - [Pricing Options on Realized Variance by Peter Carr (2005)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=684087)
      - [Parameter risk in the Black and Scholes model by Marc Henrard (2003)](https://www.researchgate.net/publication/23749495_Parameter_risk_in_the_Black_and_Scholes_model)
      - [FAQ’s in Option Pricing Theory by Peter Carr (2005)](https://www.researchgate.net/profile/Peter-Carr-4/publication/2335550_FAQ's_in_Option_Pricing_Theory/links/559ee07908ae03c44a5cdc68/FAQs-in-Option-Pricing-Theory.pdf)
        - IX Which volatility should one hedge at - historical or implied?
2. [On the Risk of Stocks in the Long Run](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5771)
   1. This paper examines the proposition that investing in common stocks is less risky the longer an investor plans to hold them. If the proposition were true, then the cost of insuring against earning less than the risk-free rate of interest should decline as the length of the investment horizon increases. The paper shows that the opposite is true even if stock returns are "mean-reverting" in the long run.
3. [Pricing Options using Deep Neural Networks from a Practical Perspective: a Comparative Study of Supervised and Unsupervised Learning](https://www.imperial.ac.uk/media/imperial-college/faculty-of-natural-sciences/department-of-mathematics/math-finance/Pu-Viola_Ruo_Han_01977026.pdf)
   1. [Github](https://github.com/violapu/OPNN)
   2. Supervised learning performed much better.
   3. [Optimally weighted loss functions for solving PDEs with Neural Networks](https://arxiv.org/pdf/2002.06269)
### Github Projects
1. [Pricing of Some Exotic Options](https://github.com/AliBakly/Pricing-of-Some-Exotic-Options/tree/main)
2. [Financial-Models-Numerical-Methods](https://github.com/cantaro86/Financial-Models-Numerical-Methods)
   1. Repository of quantitative finance examples
      1. [ ] Black-Scholes numerical methods (lognormal distribution, change of measure, Monte Carlo, Binomial method).
      2. [ ] The Black-Scholes PDE (PDE discretization, Implicit method, sparse matrix tutorial)
      3. [ ] Volatility tracking (Heston simulation, hypothesis testing, distribution fitting, estimation methods, GARCH(1,1), Kalman filter, Kalman smoother)

### X.com/Twitter
1. ["2) Unsophisticated traders think selling options is free money. So the big girls are massive option buyers and structurally long volatility."](https://x.com/bennpeifert/status/1878783199398273218)
2. ["The lowest-hanging fruit in sell-side derivatives research is implied-realized vol spread."](https://x.com/OneHotCode1/status/1877957089500254656)
3. ["GVV (gamma-vanna-volga) modeling."](https://x.com/bennpeifert/status/1888254737075835311)

### Online Resources
1. Moontower
   1. [Intro to Simulating Dynamically Hedged Option Positions](https://blog.moontower.ai/intro-to-simulating-dynamically-hedged-option-positions/)
2. 