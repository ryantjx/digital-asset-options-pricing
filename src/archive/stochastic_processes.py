import QuantLib as ql

class StochasticProcess:
    """
    Base class for all stochastic processes used in option pricing.

    GeneralizedBlackScholesProcess
        - BlackScholesMertonProcess - includes dividend yield
        - BlackScholesProcess
        - BlackProcess
    HestonProcess
        - BatesProcess
    HullWhiteProcess
    Merton76Process

    """
    @staticmethod
    def bsm_process(underlying, rf_rate, div_yield, sigma, calculation_date, day_count, calendar):
        """
        Create a Black-Scholes-Merton process.
        
        Args:
            underlying (float): Spot price of the underlying asset
            rf_rate (float): Risk-free interest rate
            div_yield (float): Dividend yield or funding cost
            sigma (float): Volatility of the underlying asset
            calculation_date (ql.Date): Evaluation date
            day_count (ql.DayCounter): Day counting convention
            calendar (ql.Calendar): Calendar for business days
            
        Returns:
            ql.BlackScholesMertonProcess: The configured BSM process
        """
        # print("params : ", underlying, rf_rate, div_yield, sigma, calculation_date, day_count, calendar)
        print(f"""params: 
            underlying: {underlying},
            rf_rate: {rf_rate},
            div_yield: {div_yield},
            sigma: {sigma},
            calculation_date: {calculation_date},
            day_count: {day_count},
            calendar: {calendar}""")
        
        print('Creating BSM process')
        riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, rf_rate, day_count))
        print('Risk-free term structure created')
        dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, div_yield, day_count))
        print('Dividend term structure created')
        bsVolTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, sigma, day_count))
        print('bsVolTS created')
        initialValue = ql.QuoteHandle(ql.SimpleQuote(underlying))
        return ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, bsVolTS)
    
    @staticmethod
    def heston_process(underlying, rf_rate, div_yield, v0, kappa, theta, sigma, rho, calculation_date, day_count, calendar):
        """
        Create a Heston stochastic volatility process.
        
        Args:
            underlying (float): Spot price of the underlying asset
            rf_rate (float): Risk-free interest rate
            div_yield (float): Dividend yield or funding cost
            v0 (float): Initial variance
            kappa (float): Mean reversion speed of variance
            theta (float): Long-term variance
            sigma (float): Volatility of variance (vol of vol)
            rho (float): Correlation between asset returns and variance
            calculation_date (ql.Date): Evaluation date
            day_count (ql.DayCounter): Day counting convention
            calendar (ql.Calendar): Calendar for business days
            
        Returns:
            ql.HestonProcess: The configured Heston process
        """
        riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, rf_rate, day_count))
        dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, div_yield, day_count))
        initialValue = ql.QuoteHandle(ql.SimpleQuote(underlying))
        
        # Create Heston process
        # Parameters: riskFreeTS, dividendTS, spot, v0, kappa, theta, sigma, rho
        return ql.HestonProcess(riskFreeTS, dividendTS, initialValue, v0, kappa, theta, sigma, rho)

    @staticmethod
    def bates_process(underlying, rf_rate, div_yield, v0, kappa, theta, sigma, rho, 
                     lambda_param, nu, delta, calculation_date, day_count, calendar):
        """
        Create a Bates jump-diffusion process with stochastic volatility.
        Particularly suitable for assets with continuous trading like cryptocurrencies
        that can exhibit both stochastic volatility and sudden jumps.
        
        Args:
            underlying (float): Spot price of the underlying asset
            rf_rate (float): Risk-free interest rate
            div_yield (float): Dividend yield or funding cost
            v0 (float): Initial variance
            kappa (float): Mean reversion speed of variance
            theta (float): Long-term variance
            sigma (float): Volatility of variance (vol of vol)
            rho (float): Correlation between asset returns and variance
            lambda_param (float): Jump intensity (average number of jumps per year)
            nu (float): Average jump size
            delta (float): Standard deviation of jump size
            calculation_date (ql.Date): Evaluation date
            day_count (ql.DayCounter): Day counting convention
            calendar (ql.Calendar): Calendar for business days
            
        Returns:
            ql.BatesProcess: The configured Bates process
        """
        riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, rf_rate, day_count))
        dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, div_yield, day_count))
        initialValue = ql.QuoteHandle(ql.SimpleQuote(underlying))
        
        # Create Bates process (Heston process + jumps)
        # Heston parameters: riskFreeTS, dividendTS, spot, v0, kappa, theta, sigma, rho
        # Jump parameters: lambda, nu, delta
        return ql.BatesProcess(riskFreeTS, dividendTS, initialValue, 
                              v0, kappa, theta, sigma, rho,
                              lambda_param, nu, delta)    