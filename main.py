from Classes.Stock import Stock
from Classes.Market import Market
from Classes.Stock import yahoo_finance_news_article_url
from datetime import time, datetime
from database.db import get_database
from Scraper.DynamicScraper import scrape_dynamic_links_and_articles
# from start_db import start_mongo
import time
import json

def main():
    # Start MongoDB server
    # start_mongo()
    time.sleep(5)  # Wait to ensure MongoDB is fully initialized

    # Connect to the database
    db = get_database()
    collection = db["articles"]
    
    with open("./nasdaq.json", "r") as file: 
        nasdaq_data = json.load(file)
        

    
    for corporation in nasdaq_data['corporations']:
        stock = Stock(company_name=nasdaq_data['name'], sector=)
        articles = scrape_dynamic_links_and_articles(url, total_links=10, num_threads=2)
        print(corporation['symbol'])
        
    # for article in articles:
    #     teslaStock.add_related_news()
    # collection.insert_many(articles)
    # url = "https://finance.yahoo.com/quote/TSLA/news/"
    # print(articles) 
    
    # print("Inserted document:", list(collection.find()))

def insert_articles_to_db(articles: list, collection):
    collection.insert_many(articles)
    
if __name__ == "__main__":
    main()
