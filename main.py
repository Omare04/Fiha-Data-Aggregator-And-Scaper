from Classes.Stock import Stock
from Classes.Market import Market
from datetime import time, datetime

# Create a market instance

baseURL  = "https://finance.yahoo.com/quote/"
nyse = Market(
    id=1,
    market_name="New York Stock Exchange",
    location="New York, USA",
    time_open=time(9, 30),  # 9:30 AM
    time_close=time(16, 0),  # 4:00 PM
    timezone="EST"
)

current_time = datetime.now().time()
is_market_open = nyse.is_open(current_time)

# Display market information
nyse.display_info()
print(f"Is the market open now? {'Yes' if is_market_open else 'No'}")


stock = Stock("TSLA", "Tesla Inc.", "Automotive", 890_000_000_000, sentiment_score=0.75)
stock.add_related_news("Tesla expands in China with new deal", 0.9)
stock.add_related_news("Concerns over Tesla's supply chain disruptions", -0.3)
stock.add_related_stock("SPCE", 0.2)  
stock.add_related_stock("AAPL", 0.1)  
stock.display_info()
