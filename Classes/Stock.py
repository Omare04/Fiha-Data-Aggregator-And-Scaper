from pymongo.collection import Collection
from Classes import Article


class Stock: 
    def __init__(self, ticker, company_name, sector, industry, market_cap, market, institutional_shareholders, mutual_fund_shareholders, price={0.0,""}, sentiment_score=0.0):
        self.ticker = ticker
        self.company_name = company_name
        self.sector = sector
        self.industry = industry
        self.market_cap = market_cap
        self.sentiment_score = sentiment_score
        self.market = market
        self.price = price
        self.related_news = []  
        self.related_stocks = {}  
        self.institutional_shareholders = institutional_shareholders
        self.mutual_fund_shareholders = mutual_fund_shareholders
        self.product_involvement_areas = []

    def __str__(self):
        return f"""
        Ticker: {self.ticker}
        Company Name: {self.company_name}
        Sector: {self.sector}
        Industry: {self.industry}
        Market Cap: {self.market_cap}
        Market: {self.market}
        Price: {self.price}
        Sentiment Score: {self.sentiment_score}
        Institutional Shareholders: {self.institutional_shareholders}
        Mutual Fund Shareholders: {self.mutual_fund_shareholders}
        """

    def to_dict(self):
        """Convert Stock instance to a dictionary for MongoDB insertion."""
        return {
            "ticker": self.ticker,
            "company_name": self.company_name,
            "sector": self.sector,
            "industry": self.industry,
            "market_cap": self.market_cap,
            "sentiment_score": self.sentiment_score,
            "market": self.market,
            "price": list(self.price),  # Convert set to list
            "related_news": [article.to_dict() for article in self.related_news],
            "related_stocks": self.related_stocks,
            "institutional_shareholders": self.institutional_shareholders,
            "mutual_fund_shareholders": self.mutual_fund_shareholders,
            "product_involvement_areas": self.product_involvement_areas
        }

    @staticmethod
    def insert_stock(stock: 'Stock', collection: Collection):
        """Insert a single Stock object into the MongoDB collection."""
        collection.insert_one(stock.to_dict())
        print(f"Inserted stock: {stock.ticker}")

    @staticmethod
    def insert_stocks(stocks: list['Stock'], collection: Collection):
        """Insert multiple Stock objects into the MongoDB collection."""
        collection.insert_many([stock.to_dict() for stock in stocks])
        print(f"Inserted {len(stocks)} stocks into MongoDB.")

    def check_if_ticker_exists_in_db(db, ticker):
        collection = db["stocks"]
        result = collection.find_one({"ticker": ticker})
        return result is not None
    
        
        