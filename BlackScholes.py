from numpy import exp,sqrt,log
from scipy.stats import norm


class BlackScholes:
    def __init__(
            self,
            time_to_maturity: float,
            strike: float,
            current_price: float,
            volatitly: float,
            interest_rate: float,
    ):
        
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatitly
        self.interest_rate = interest_rate

    def  run(
            self,
    ):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate


        d_pos = (
            (
                1/(volatility * sqrt(time_to_maturity))
        )*(
            log(current_price / strike) + (interest_rate + (0.5 * volatility ** 2)) * time_to_maturity
        )
        )

        d_neg = (
            d_pos - (sqrt(time_to_maturity) * volatility)
        )

        call_price = (
            current_price * norm.cdf(d_pos) - (
                strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d_neg)
            )
        )

        put_price = (
            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d_neg)
        )- current_price * norm.cdf( -d_pos)

        self.call_price = call_price
        self.put_price = put_price

        #THE GREEKS
        


