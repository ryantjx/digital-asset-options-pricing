import QuantLib as ql

class Pricer:
    def price():
        pass

class AnalyticEuropeanPricer(Pricer):
    def __init__(self, option_type = ql.Option.Call):
        self.option_type = option_type
        print(f"Created {AnalyticEuropeanPricer.__name__} and option type {self.option_type}")
    
    def price(self, calculation_date, underlying, strike, sigma, rf_rate, days_to_maturity, div):
        maturity_date = ql.Date(calculation_date.serialNumber() + int(days_to_maturity))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        ql.Settings.instance().evaluationDate = calculation_date

        bsm_process = ql.BlackScholesMertonProcess(
            s0 = ql.QuoteHandle(ql.SimpleQuote(underlying)),
            dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, div, day_count)),
            riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, rf_rate, day_count)),
            volTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, sigma, day_count)),
        )
        payoff = ql.PlainVanillaPayoff(self.option_type, strike)
        europeanExcercise = ql.EuropeanExercise(maturity_date)
        europeanOption = ql.VanillaOption(payoff, europeanExcercise)

        engine = ql.AnalyticEuropeanEngine(bsm_process)
        europeanOption.setPricingEngine(engine)

        return europeanOption.NPV()
    
class MCEuropeanPricer(Pricer):
    def __init__(self, steps, num_paths, option_type = ql.Option.Call, seed = 42):
        self.steps = steps
        self.num_paths = num_paths
        self.seed = seed
        self.option_type = option_type
        print(f"Created {MCEuropeanPricer.__name__} and option type {self.option_type}")
    
    def price(self, calculation_date, underlying, strike, sigma, rf_rate, days_to_maturity, div):
        maturity_date = ql.Date(calculation_date.serialNumber() + int(days_to_maturity))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        ql.Settings.instance().evaluationDate = calculation_date

        bsm_process = ql.BlackScholesMertonProcess(
            s0 = ql.QuoteHandle(ql.SimpleQuote(underlying)),
            dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, div, day_count)),
            riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, rf_rate, day_count)),
            volTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, sigma, day_count)),
        )
        payoff = ql.PlainVanillaPayoff(self.option_type, strike)
        europeanExcercise = ql.EuropeanExercise(maturity_date)
        europeanOption = ql.VanillaOption(payoff, europeanExcercise)

        engine = ql.MCEuropeanEngine(bsm_process, "pseudorandom", self.steps, requiredSamples=self.num_paths, seed=self.seed)
        europeanOption.setPricingEngine(engine)

        return europeanOption.NPV()
    
class BinomialEuropeanPricer(Pricer):
    def __init__(self, steps, option_type = ql.Option.Call):
        self.steps = steps
        self.option_type = option_type
        print(f"Created {BinomialEuropeanPricer.__name__} and option type {self.option_type}")
    
    def price(self, calculation_date, underlying, strike, sigma, rf_rate, days_to_maturity, div):
        maturity_date = ql.Date(calculation_date.serialNumber() + int(days_to_maturity))
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        ql.Settings.instance().evaluationDate = calculation_date

        bsm_process = ql.BlackScholesMertonProcess(
            s0 = ql.QuoteHandle(ql.SimpleQuote(underlying)),
            dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, div, day_count)),
            riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, rf_rate, day_count)),
            volTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, sigma, day_count)),
        )
        payoff = ql.PlainVanillaPayoff(self.option_type, strike)
        europeanExcercise = ql.EuropeanExercise(maturity_date)
        europeanOption = ql.VanillaOption(payoff, europeanExcercise)

        engine = ql.BinomialVanillaEngine(bsm_process, "crr", self.steps)
        europeanOption.setPricingEngine(engine)

        return europeanOption.NPV()