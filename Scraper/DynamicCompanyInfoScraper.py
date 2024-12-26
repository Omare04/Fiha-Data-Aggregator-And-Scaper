from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from Classes.Stock import Stock
from Scraper.DynamicArticleScraper import handle_cookie_modal
import requests

options = Options()
options.add_argument('--headless')  
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.page_load_strategy = 'eager'  
service = Service('/usr/local/bin/chromedriver')


def setup_driver(service, options):
    return webdriver.Chrome(service=service, options=options)


def scrape_market_cap(driver, ticker):
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics"
        driver.get(url)
        market_cap_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table.yf-kbx2lo"))
        )
        table_text = market_cap_element.text.strip()
        data_lines = table_text.split('\n')[1]
        headers = table_text.split('\n')[0]

        data_list = data_lines.split()[2:]
        headers = headers.split()
        market_cap_data = {}
        
        for i in range(len(data_list)):
            match = re.search(r"(\d+\.\d+[A-Z]*)", data_list[i])
            if match:
                market_cap_data[headers[i]] = match.group(1)
        
        return market_cap_data

    except Exception as e:
        print(f"Error scraping market cap: {e}")
        return None


def scrape_industry_and_sector(driver, ticker):
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/profile"
        driver.get(url)
        company_stats = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "company-stats.yf-wxp4ja"))
        )
        stats_text = company_stats.text.strip().split('\n')
        sector = industry = None
        
        for i in range(len(stats_text)):
            if "Sector:" in stats_text[i]:
                sector = stats_text[i + 1].strip()
            if "Industry:" in stats_text[i]:
                industry = stats_text[i + 1].strip()
        
        return sector, industry

    except Exception as e:
        print(f"Error scraping sector and industry: {e}")
        return None, None


def scrape_shareholders(driver, ticker):
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/holders/"
        driver.get(url)

        # Institutional Holders
        institutional_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='holders-top-institutional-holders']"))
        )
        institutional_holders = [
            row.text.split('\n')[0] for row in institutional_section.find_elements(By.TAG_NAME, "tr")
        ]
        
        # Mutual Fund Holders
        mutual_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='holders-top-mutual-fund-holders']"))
        )
        mutual_holders = [
            row.text.split('\n')[0] for row in mutual_section.find_elements(By.TAG_NAME, "tr")
        ]

        return institutional_holders, mutual_holders

    except Exception as e:
        print(f"Error scraping shareholders: {e}")
        return None, None


def scrape_stock_price_and_time(driver, ticker):
    try:
        driver.get(f"https://finance.yahoo.com/quote/{ticker}")
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"fin-streamer[data-symbol='{ticker}'] span"))
        )
        market_time_element = driver.find_element(By.CSS_SELECTOR, "span.base.yf-ipw1h0")
        
        return price_element.text.strip(), market_time_element.text.strip()
    
    except Exception as e:
        print(f"Error scraping price/time: {e}")
        return None, None
    
def check_if_exists(driver, ticker):
    try:
        driver.get(f"https://finance.yahoo.com/lookup/?s={ticker}")
        

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".noData.yf-wnifss"))
        )
        print("This stock does not exist on yahoo finance")
        return False
    
    except Exception:
        return True


def check_if_exists_url(driver, ticker):
    target_url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics"
    driver.get(target_url)
    
    # Wait for page load and check final URL
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    current_url = driver.current_url
    
    if target_url not in current_url:
        return False
    else:
        print(f"{ticker} exists.")
        return True


def scrape_company_information(ticker, company_name, additional_info):
    driver = setup_driver(service, options)
    handle_cookie_modal(driver, 0)
    
    try:
        if check_if_exists(driver, ticker):
            start_time = time.time()
            
            market_cap = scrape_market_cap(driver, ticker)
            sector, industry = additional_info["sector"], additional_info["industry"] if additional_info["sector"] and additional_info["industry"] else scrape_industry_and_sector(driver, ticker)
            institutional, mutual = scrape_shareholders(driver, ticker)
            stock_price, market_time = scrape_stock_price_and_time(driver, ticker)

            if market_cap and sector and industry and stock_price:
                company_info = Stock(
                    ticker=ticker,
                    company_name=company_name,
                    sector=sector,
                    industry=industry,
                    market=" ",
                    institutional_shareholders=institutional,
                    mutual_fund_shareholders=mutual,
                    market_cap=market_cap,
                    price=(stock_price, market_time)
                )
                
                elapsed_time = time.time() - start_time
                print(f"Scraping completed in {elapsed_time:.2f} seconds.")
                print(f"Company Info: {company_info}")
                
                return company_info
            
            else:
                print(f"Skipping {ticker} - Missing critical data")
                return None
        
        else:
            print(f"{ticker} does not exist.")
            return None
    
    except Exception as e:
        print(f"Error scraping {ticker}: {e}")
        return None
    
    finally:
        driver.quit()



if __name__ == "__main__":
    driver = setup_driver(service, options)
    result = check_if_exists_url(driver, "AAPL")
    print(result)
    # ticker = "AAPL"
    # company_name = "Tesla"
    # scrape_company_information(ticker, company_name)
