from Classes.Stock import Stock
from Classes.Market import Market
from datetime import time, datetime
from Scraper.DynamicCompanyInfoScraper import scrape_company_information
from Scraper.DynamicArticleScraper import scrape_article_information
from database.db import get_database
from Scraper.DynamicArticleScraper import scrape_dynamic_links_and_articles
# from start_db import start_mongo
import time
import json
import requests
import os 


#Create a bullish and bearish score for each stock
# C4WM5R86421K4HGQ

def main():
    # Start MongoDB server
    # start_mongo()
    # time.sleep(5)  # Wait to ensure MongoDB is fully initialized

    db = get_database()
    with open("./nasdaq100.json", "r") as file: 
        nasdaq100 = json.load(file)
        
    insert_articles_to_db(nasdaq100, db)
        

def insert_stocks_to_db(data, db):  
    for corporation in data:
        ticker = corporation["Symbol"]
        company_name = corporation["Security"]
        additional_info = {"industry":corporation["GICS Sub-Industry"], "sector": corporation["GICS Sector"]}

        if Stock.check_if_ticker_exists_in_db(db, ticker):
            continue
        
        print("This is the company that you're scraping:", ticker)
        
        company_info = scrape_company_information(ticker, company_name, additional_info)
        
        if company_info:
            db["stocks"].insert_one(company_info.to_dict())
            print(f"{ticker} inserted into the database")
        else:
        
            print(f"Skipping {ticker} - No data to insert")

        # print(stock)
        # url = stock.yahoo_finance_url("/news/")
        # articles = scrape_dynamic_links_and_articles(url, total_links=10, num_threads=2)
        
def insert_articles_to_db(data, db): 
    for corporation in data:
        ticker = corporation["symbol"]  
        try:
            if Stock.check_if_ticker_exists_in_db(db, ticker):
                url = f"https://finance.yahoo.com/quote/{ticker}/news/"

                articles = scrape_dynamic_links_and_articles(url,ticker=ticker, num_threads=2, total_links=20)
                print(articles)

                if articles: 
                    db["articles"].insert_many([{"article": article, "company": ticker} for article in articles])
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
                
            
        
if __name__ == "__main__":
    main()
