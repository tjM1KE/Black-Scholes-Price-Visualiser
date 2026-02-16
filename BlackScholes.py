from numpy import exp,sqrt,log
from scipy.stats import norm


class BlackScholes:
    def __init__(
            self,
            time_to_maturity: float,
            strike: float,
            current_price: float,
            volatility: float,
            interest_rate: float,
    ):
        
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
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

        #delta
        self.call_delta = norm.cdf(d_pos)
        self.put_delta = norm.cdf(d_pos) - 1

        #gamma
        self.call_gamma = norm.pdf(d_pos) / (
            current_price * volatility * sqrt(time_to_maturity)
        )
        self.put_gamma = self.call_gamma

        #vega
        self.call_vega = current_price * norm.pdf(d_pos) * sqrt(time_to_maturity)
        self.put_vega = self.call_vega

        #theta
        self.call_theta = (
            (-1 * strike * norm.pdf(d_pos) * volatility) / (
                2 * sqrt(time_to_maturity)
            )
        ) - (
            interest_rate * strike * exp(-1 * interest_rate * time_to_maturity) * norm.cdf(d_neg)
        )
        self.put_theta = (
            (-1 * strike * norm.pdf(d_pos) * volatility) / (
                2 * sqrt(time_to_maturity)
            )
        ) + (
            interest_rate * strike * exp(-1 * interest_rate * time_to_maturity) * norm.cdf(-d_neg)
        )




        #rho


        
if __name__ == "__main__":
    time_to_maturity = 2
    strike = 90
    current_price = 100
    volatility = 0.2
    interest_rate = 0.05

    #Black Scholes

    BS = BlackScholes(
            time_to_maturity = time_to_maturity,
            strike = strike,
            current_price = current_price,
            volatility = volatility,
            interest_rate = interest_rate)
    BS.run()


