class StockOption:
    def __init__(self, option_type, stock_price, strike_price, premium, contract_name, implied_volatility):
        if option_type not in {"call", "put"}:
            raise ValueError("option_type must be 'call' or 'put'")
        if stock_price < 0 or strike_price < 0 or premium < 0 or implied_volatility < 0:
            raise ValueError("stock_price, strike_price, premium, and implied_volatility must be non-negative")
        self.option_type = option_type
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.premium = premium
        self.contract_name = contract_name
        self.implied_volatility = implied_volatility


    def is_in_the_money(self) -> bool:
        # Determines if the option is "in the money."
        # For a call option, it's in the money if the stock price exceeds the strike price.
        # For a put option, it's in the money if the stock price is below the strike price.
        if self.option_type == "call":
            return self.stock_price > self.strike_price
        elif self.option_type == "put":
            return self.stock_price < self.strike_price

    def intrinsic_value(self) -> float:
        # Calculates the intrinsic value of the option.
        # For a call option, it's the difference between the stock price and the strike price (if positive).
        # For a put option, it's the difference between the strike price and the stock price (if positive).
        if self.option_type == "call":
            return max(0, self.stock_price - self.strike_price)
        elif self.option_type == "put":
            return max(0, self.strike_price - self.stock_price)

    def potential_profit(self) -> float:
        # Calculates the potential profit of the option.
        # If the option is in the money, it's the intrinsic value minus the premium.
        # If it's out of the money, the loss is the premium paid.
        if self.is_in_the_money():
            return self.intrinsic_value() - self.premium
        else:
            return -self.premium

# A call option gives the holder the right to buy a stock at a specific price (strike price) within a set timeframe,
# while a **put option** gives the right to sell a stock at the strike price. 
# The **premium** is the cost paid to purchase the option, 
# and the **strike price** is the predetermined price at which the stock can be bought (call) or sold (put).
