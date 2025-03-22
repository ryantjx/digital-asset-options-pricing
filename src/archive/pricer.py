import QuantLib as ql
from ..enums import OptionType, OptionColumns
from ..models.stochastic_processes import StochasticProcess
import numpy as np
from tqdm import tqdm

"""
Done (flat BSM stochastic process)
1. MCEuropeanPricer
2. BinomialEuropeanPricer
3. AnalyticEuropeanPricer
4. FdBlackScholesVanillaPricer

To build
4. MCEuropeanHestonEngine
5. FdHestonVanillaEngine
6. AnalyticPTDHestonEngine
7. AnalyticEuropeanEngine

Problems to solve
- How can i customize the stochastic process to improve the pricing engine? 
    - non flat yield structure?
"""

class Pricer:
    def price_all(self, df, use_tqdm = False):
        prices = np.zeros(df.shape[0])

        iterator = df.iterrows()

        if use_tqdm:
            iterator = tqdm(iterator, total=df.shape[0])

        for i, row in iterator:
            strike = row[OptionColumns.STRIKE]
            sigma = row[OptionColumns.SIGMA]
            div = row[OptionColumns.DIVIDEND_RATE]
            days_to_maturity = row[OptionColumns.DAYS_TO_MATURITY]
            rf_rate = row[OptionColumns.RF_RATE]
            underlying = row[OptionColumns.UNDERLYING]

            prices[i] = self.price(underlying=underlying, 
                                   strike=strike, sigma=sigma, 
                                   days_to_maturity=days_to_maturity, 
                                   rf_rate=rf_rate, 
                                   div=div)
        return prices
    
class MCEuropeanPricer(Pricer):
    """
    Creates a Monte Carlo simulation engine for European options.
    This engine simulates multiple price paths and averages the payoffs to price options.
    Allows for more flexibility than analytical solutions but is computationally intensive.
    
    Args:
        process (ql.GeneralizedBlackScholesProcess): Process describing the underlying's behavior
        timesteps (int): Number of timesteps in each simulated path
        required_samples (int): Number of Monte Carlo paths to simulate
        seed (int): Random seed for reproducibility
            
    Returns:
        ql.MCEuropeanEngine: A Monte Carlo-based pricing engine
    """
    def __init__(self, calculation_date, option_type, steps, num_paths, seed = 42):
        self.calculation_date = calculation_date
        self.option_type = OptionType.ql_type(option_type)
        self.steps = steps
        self.num_paths = num_paths
        self.seed = seed
        print(f"Created {MCEuropeanPricer.__name__} on {calculation_date} and option type {self.option_type}")
    
    def price(self, underlying, strike, sigma, maturity, rf_rate, div):
        maturity_date = ql.Date(self.calculation_date.serialNumber() + int(maturity))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        ql.Settings.instance().evaluationDate = self.calculation_date

        bsm_process = StochasticProcess.bsm_process(
            underlying=underlying, 
            rf_rate=rf_rate, 
            div_yield=div, 
            sigma=sigma, 
            calculation_date=self.calculation_date, 
            day_count=day_count, 
            calendar=calendar)
                
        payoff = ql.PlainVanillaPayoff(self.option_type, strike)
        europeanExercise = ql.EuropeanExercise(maturity_date)
        europeanOption = ql.VanillaOption(payoff, europeanExercise)

        engine = ql.MCEuropeanEngine(bsm_process, "pseudorandom", self.steps, requiredSamples=self.num_paths, seed=self.seed)
        europeanOption.setPricingEngine(engine)

        option_price = europeanOption.NPV()
        print(f"MCEuropeanEngine Option Pricing:")
        # print(f"  Underlying price: {underlying:.2f}")
        # print(f"  Strike price: {strike:.2f}")
        # print(f"  Volatility: {sigma:.2%}")
        # print(f"  Maturity: {maturity} days (until {maturity_date})")
        # print(f"  Risk-free rate: {rf_rate:.2%}")
        # print(f"  Dividend yield: {div:.2%}")
        # print(f"  Valuation date: {self.calculation_date}")
        print(f"  Option price: {option_price:.4f}")
        return option_price

class BinomialEuropeanPricer(Pricer):
    def __init__(self, calculation_date, option_type, steps):
        self.calculation_date = calculation_date
        self.option_type = OptionType.ql_type(option_type)
        self.steps = steps
        print(f"Created {BinomialEuropeanPricer.__name__} on {calculation_date} and option type {self.option_type}")
    
    def price(self, underlying, strike, sigma, maturity, rf_rate, div):
        maturity_date = ql.Date(self.calculation_date.serialNumber() + int(maturity))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        ql.Settings.instance().evaluationDate = self.calculation_date

        bsm_process = StochasticProcess.bsm_process(
            underlying=underlying, 
            rf_rate=rf_rate, 
            div_yield=div, 
            sigma=sigma, 
            calculation_date=self.calculation_date, 
            day_count=day_count, 
            calendar=calendar)
        
        payoff = ql.PlainVanillaPayoff(self.option_type, strike)
        europeanExercise = ql.EuropeanExercise(maturity_date)
        europeanOption = ql.VanillaOption(payoff, europeanExercise)

        engine = ql.BinomialVanillaEngine(bsm_process, "crr", self.steps)
        europeanOption.setPricingEngine(engine)
        option_price = europeanOption.NPV()
        option_type_name = "Call" if self.option_type == ql.Option.Call else "Put"
        print(f"BinomialVanillaEngine {option_type_name} Option Pricing:")
        # print(f"  Underlying price: {underlying:.2f}")
        # print(f"  Strike price: {strike:.2f}")
        # print(f"  Volatility: {sigma:.2%}")
        # print(f"  Maturity: {maturity} days (until {maturity_date})")
        # print(f"  Risk-free rate: {rf_rate:.2%}")
        # print(f"  Dividend yield: {div:.2%}")
        # print(f"  Valuation date: {self.calculation_date}")
        print(f"  Option price: {option_price:.4f}")
        return europeanOption.NPV()

class AnalyticEuropeanPricer(Pricer):
    """
    Black-Scholes-Merton closed-form solution for European options.
    
    Best for: Standard European vanilla options under BSM assumptions.
    Advantages: Extremely fast computation with exact solution.
    Limitations: Only works for European exercise, requires BSM assumptions.
    """
    def __init__(self, calculation_date, option_type):
        self.calculation_date = calculation_date
        self.option_type = option_type
        print(f"Created {AnalyticEuropeanPricer.__name__} on {calculation_date} and option type {self.option_type}")

    def price(self, underlying, strike, sigma, maturity, rf_rate, div):
        maturity_date = ql.Date(self.calculation_date.serialNumber() + int(maturity))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        ql.Settings.instance().evaluationDate = self.calculation_date

        bsm_process = StochasticProcess.bsm_process(
            underlying=underlying, 
            rf_rate=rf_rate, 
            div_yield=div, 
            sigma=sigma, 
            calculation_date=self.calculation_date, 
            day_count=day_count, 
            calendar=calendar)
        
        payoff = ql.PlainVanillaPayoff(self.option_type, strike)
        europeanExercise = ql.EuropeanExercise(maturity_date)
        europeanOption = ql.VanillaOption(payoff, europeanExercise)

        engine = ql.AnalyticEuropeanEngine(bsm_process)
        europeanOption.setPricingEngine(engine)

        option_price = europeanOption.NPV()

        # Comprehensive print statement
        option_type_name = "Call" if self.option_type == ql.Option.Call else "Put"
        print(f"AnalyticEuropeanEngine(BSM) {option_type_name} Option Pricing:")
        # print(f"  Underlying price: {underlying:.2f}")
        # print(f"  Strike price: {strike:.2f}")
        # print(f"  Volatility: {sigma:.2%}")
        # print(f"  Maturity: {maturity} days (until {maturity_date})")
        # print(f"  Risk-free rate: {rf_rate:.2%}")
        # print(f"  Dividend yield: {div:.2%}")
        # print(f"  Valuation date: {self.calculation_date}")
        print(f"  Option price: {option_price:.4f}")
        
        # # Calculate additional Greeks for verification
        # delta = europeanOption.delta()
        # gamma = europeanOption.gamma()
        # theta = europeanOption.theta()
        # vega = europeanOption.vega()
        # print(f"  Greeks:")
        # print(f"    Delta: {delta:.4f}")
        # print(f"    Gamma: {gamma:.6f}")
        # print(f"    Theta: {theta:.6f}")
        # print(f"    Vega: {vega:.6f}")
        return option_price
    
class FdBlackScholesVanillaPricer(Pricer):
    """
    Creates a finite difference method engine for European options.
    This engine discretizes the Black-Scholes PDE and solves it numerically.
    Offers a good balance between speed and flexibility, and can handle various features.
    
    Args:
        process (ql.GeneralizedBlackScholesProcess): Process describing the underlying
        time_grid (int): Number of time steps in the finite difference grid
        stock_grid (int): Number of price levels in the finite difference grid
            
    Returns:
        ql.FdBlackScholesVanillaEngine: A finite difference pricing engine
    """
    def __init__(self, calculation_date, option_type, time_grid, stock_grid):
        self.calculation_date = calculation_date
        self.option_type = OptionType.ql_type(option_type)
        self.time_grid = time_grid
        self.stock_grid = stock_grid
        print(f"Created {FdBlackScholesVanillaPricer.__name__} with time grid {time_grid} and stock grid {stock_grid}")
    
    def price(self, underlying, strike, sigma, maturity, rf_rate, div):
        maturity_date = ql.Date(self.calculation_date.serialNumber() + int(maturity))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        ql.Settings.instance().evaluationDate = self.calculation_date

        bsm_process = StochasticProcess.bsm_process(underlying, rf_rate, div, sigma, self.calculation_date, day_count, calendar)

        payoff = ql.PlainVanillaPayoff(self.option_type, strike)
        europeanExercise = ql.EuropeanExercise(maturity_date)
        europeanOption = ql.VanillaOption(payoff, europeanExercise)

        engine = ql.FdBlackScholesVanillaEngine(bsm_process, self.time_grid, self.stock_grid)
        europeanOption.setPricingEngine(engine)
        option_price = europeanOption.NPV()

        option_type_name = "Call" if self.option_type == ql.Option.Call else "Put"
        print(f"FdBlackScholesVanillaEngine {option_type_name} Option Pricing:")
        # print(f"  Underlying price: {underlying:.2f}")
        # print(f"  Strike price: {strike:.2f}")
        # print(f"  Volatility: {sigma:.2%}")
        # print(f"  Maturity: {maturity} days (until {maturity_date})")
        # print(f"  Risk-free rate: {rf_rate:.2%}")
        # print(f"  Dividend yield: {div:.2%}")
        # print(f"  Valuation date: {self.calculation_date}")
        print(f"  Option price: {option_price:.4f}")
        return option_price