class Stock: 
    def __init__(self, ticker, company_name, sector, volume, market_cap, market, price,sentiment_score=0.0):
        self.ticker = ticker
        self.company_name = company_name
        self.sector = sector
        self.market_cap = market_cap
        self.sentiment_score = sentiment_score
        self.market = market
        self.price = price
        self.volume = volume
        self.related_news = []  
        self.related_stocks = {}  
        self.stakeholders = {}
        self.mutual_fund_holders = {}
        self.product_involvement_areas = []

    def add_stakeholder(self, stakeholder_obj):
        self.stakeholders[stakeholder_obj.name] = {
            "shares": stakeholder_obj.shares,
            "percentage": stakeholder_obj.percentage,
            "value": stakeholder_obj.value,
        }

    def update_stakeholder(self, name, shares, percentage, value):
        if name in self.stakeholders:
            self.stakeholders[name] = {
                "shares": shares,
                "percentage": percentage,
                "value": value,
            }

    def add_mutual_fund_holder(self, mutual_fund_obj):
        self.mutual_fund_holders[mutual_fund_obj.fund_name] = {
            "shares": mutual_fund_obj.shares,
            "percentage": mutual_fund_obj.percentage,
            "value": mutual_fund_obj.value,
            "fund_manager": mutual_fund_obj.fund_manager,
        }

    def update_mutual_fund_holder(self, fund_name, shares, percentage, value):
        if fund_name in self.mutual_fund_holders:
            self.mutual_fund_holders[fund_name] = {
                "shares": shares,
                "percentage": percentage,
                "value": value,
                "fund_manager": self.mutual_fund_holders[fund_name]["fund_manager"],
            }

    def display_stakeholders(self):
        print(f"Stakeholders for {self.company_name} ({self.ticker}):")
        for name, details in self.stakeholders.items():
            print(f"  Name: {name}")
            print(f"    Shares: {details['shares']}")
            print(f"    Ownership Percentage: {details['percentage']:.2f}%")
            print(f"    Value: ${details['value']:,.2f}")

    def display_mutual_fund_holders(self):
        print(f"Mutual Fund Holders for {self.company_name} ({self.ticker}):")
        for fund_name, details in self.mutual_fund_holders.items():
            print(f"  Fund Name: {fund_name}")
            print(f"    Shares: {details['shares']}")
            print(f"    Ownership Percentage: {details['percentage']:.2f}%")
            print(f"    Value: ${details['value']:,.2f}")
            print(f"    Fund Manager: {details['fund_manager']}")
            
    def add_related_news(self, news_title, sentiment):
        self.related_news.append({'title': news_title, 'sentiment': sentiment})

    def add_related_stock(self, related_ticker, relationship_score):
        self.related_stocks[related_ticker] = relationship_score

    def display_info(self):
        print(f"Ticker: {self.ticker}")
        print(f"Company Name: {self.company_name}")
        print(f"Sector: {self.sector}")
        print(f"Market Cap: ${self.market_cap:,.2f}")
        print(f"Sentiment Score: {self.sentiment_score}")
        print("Related News:")
        for news in self.related_news:
            print(f"  - {news['title']} (Sentiment: {news['sentiment']})")
        print("Related Stocks:")
        for stock, score in self.related_stocks.items():
            print(f"  - {stock}: Relationship Score {score}")
