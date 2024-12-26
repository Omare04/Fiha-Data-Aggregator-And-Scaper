from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from Classes.Article import Article
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import functools
# Global Selenium options and service
options = Options()
options.add_argument('--headless') 
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument('--disable-gpu')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service('/usr/local/bin/chromedriver')


def setup_driver(service, options):
    return webdriver.Chrome(service=service, options=options)


def check_continue_reading_button(driver, thread_id, link):
    try:
        driver.get(link)
        
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # Handle bot detection 
        if "<body></body>" in driver.page_source:
            print("Detected bot block - page did not load properly.")
            return True
        
        button_xpath = "//button[contains(@class, 'continue-reading-button')]"
        
        # Scroll once to load potential dynamic
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
        time.sleep(1)
        
        #incremental scroll 
        max_attempts = 4
        scroll_attempts = 0
        
        while scroll_attempts < max_attempts:
            driver.execute_script("window.scrollBy(0, 600);") 
            scroll_attempts += 1
            time.sleep(0.3)

            # Look for button during each scroll attempt
            try:
                button = driver.find_element(By.XPATH, button_xpath)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                
            
                WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                print(f"Thread-{thread_id}: 'Continue Reading' button detected. Skipping article at {link}")
                return None
            except NoSuchElementException:
                continue

        print(f"Thread-{thread_id}: No 'Continue Reading' button found for link {link}. Continuing...")
        return True

    except Exception as e:
        print(f"Thread-{thread_id}: Unexpected error for link {link}: {e}")
        return True


def handle_cookie_modal(driver, thread_id):
    """Handles cookie modal if present."""
    try:
        reject_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "reject-all"))
        )
        reject_button.click()
    except Exception:
        print(f"Thread-{thread_id}: No cookie modal.")

def extract_links(driver, thread_id, number_of_links=10):
    """Extracts a specified number of unique article links."""
    links = []
    while len(links) < number_of_links:
        anchors = driver.find_elements(By.CSS_SELECTOR, "a.subtle-link.fin-size-small.thumb")
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if href and href.startswith("https://finance.yahoo.com") and href not in links:
                links.append(href)
            if len(links) >= number_of_links:
                break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Avoid server overload
    return links

def extract_title(driver, thread_id, link):
    try: 
        title_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cover-title.yf-1at0uqp"))
                )
        title = title_element.text.strip() if title_element else None
        
        if title: 
            return title
        else:
            print("No title found")
            return None
    except Exception as e:
        print(f"Thread-{thread_id}: Error scraping title for this article at {link}")
        
def extract_author_date_published(driver, thread_id, link):
    try:
        wait = WebDriverWait(driver, 10)  
        author_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "byline-attr-author.yf-1k5w6kz"))
        )
        author = author_element.text.strip() if author_element else None

        date_published_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "byline-attr-meta-time"))
        )
        date_published = date_published_element.get_attribute("datetime") if date_published_element else None

        if author:
            return author, date_published
        else:
            print(f"Thread-{thread_id}: No author found for this article at {link}")
            return None, date_published

    except TimeoutException:
        print(f"Thread-{thread_id}: Timeout while scraping author or date published at {link}.")
        return None, None
    except NoSuchElementException:
        print(f"Thread-{thread_id}: Author or date element not found at {link}.")
        return None, None
    except Exception as e:
        print(f"Thread-{thread_id}: Error scraping author or date published at {link}: {e}")
        return None, None
        
def handle_story_continues(driver, thread_id, link):
    
    try:
        story_continues_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "secondary-btn.fin-size-large.readmore-button.rounded.yf-15mk0m"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", story_continues_button)
        try:
            story_continues_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", story_continues_button)
        print(f"Thread-{thread_id}: 'Story continues' button clicked for {link}.")
    except Exception:
        print(f"Thread-{thread_id}: No 'Story continues' button for {link}.")

def scrape_article_information(driver, thread_id, link):
    try:
        driver.get(link)
        handle_story_continues(driver, thread_id, link)
        article_content = ""

        paragraphs = driver.find_elements(By.CLASS_NAME, "yf-1pe5jgt")
        for paragraph in paragraphs:
            article_content += paragraph.text.strip() + " "

        if article_content.strip():
            return article_content.strip()
        else:
            print(f"Thread-{thread_id}: No content found for {link}.")
            return None
    except Exception as e:
        print(f"Thread-{thread_id}: Error scraping article at {link}: {e}")
        return None

def scrape_links_and_articles(url, results, thread_id, number_of_links, db, ticker, driver):
    try:
        print(f"Thread-{thread_id}: Starting...")
        driver.get(url)

        handle_cookie_modal(driver, thread_id)
        links = extract_links(driver, thread_id, number_of_links)
        print(f"Thread-{thread_id}: Extracted {len(links)} links.")
        
        scraped_articles = Article.get_article_urls_by_ticker(db, ticker)

        for link in links:
            
            if scraped_articles and link in scraped_articles:
                print(f"Article exists in database, skipping {link}")
                continue
            
            can_access_article = check_continue_reading_button(driver, thread_id, link=link)
            if not can_access_article:  
                continue
            
            article_content = scrape_article_information(driver, thread_id, link)
            if not article_content:  
                print(f"No content found for {link}, skipping.")
                continue
                
            author, date_published = extract_author_date_published(driver, thread_id, link)
            title = extract_title(driver, thread_id, link)
            
            if author and date_published and title:
                article = Article(
                    title=title,
                    content=article_content,
                    author=author,
                    date_published=date_published,
                    url=link
                )
                results.append(article.to_dict())
                print(f"Article {article.url} Scraped, and added to results list")
            else:
                print(f"Missing metadata for {link}, skipping.")

    finally:
        print(f"Thread-{thread_id}: Done.")
        
def scrape_dynamic_links_and_articles(url,ticker ,total_links=20, num_threads=1, db=None, driver=None):
    results = []
    threads = []
    links_per_thread = total_links // num_threads

    start_time = time.time()
    print(f"Scraping articles for {ticker}")

    for thread_id in range(num_threads):
        thread = threading.Thread(
            target=scrape_links_and_articles, 
            args=(url, results, thread_id, links_per_thread, db, ticker, driver)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Collected {len(results)} articles in {elapsed_time:.2f} seconds.")  
    return results

#Test Individual functions for consistency
if __name__ == "__main__":
    driver  = setup_driver(service, options)
    url = "https://finance.yahoo.com/quote/TSLA/news/"
    result = check_continue_reading_button(driver, 0, "https://finance.yahoo.com/m/4205eaa9-f620-3a0b-a81a-0e82c7c9fd0b/magnificent-seven-stocks-.html")
    print(f"this is the result: {result}")
