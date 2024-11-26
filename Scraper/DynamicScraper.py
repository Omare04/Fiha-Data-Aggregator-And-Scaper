from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

# Global Selenium options and service
options = Options()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')
service = Service('/usr/local/bin/chromedriver')


def setup_driver(service, options):
    """Sets up and returns a Selenium WebDriver."""
    return webdriver.Chrome(service=service, options=options)


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

def handle_story_continues(driver, thread_id, link):
    """Handles 'Story continues' or 'Continue Reading' buttons on article pages."""
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

def handle_external_articles(driver, thread_id, link):
    
    return 

def scrape_article(driver, thread_id, link):
    """Scrapes the content of an article given its link."""
    try:
        driver.get(link)
        handle_story_continues(driver, thread_id, link)
        article_content = ""

        # Extract all visible paragraphs
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

def scrape_links_and_articles(url, results, thread_id, service, options, number_of_links):
    """Main function to scrape links and articles from the given URL."""
    driver = setup_driver(service, options)
    try:
        print(f"Thread-{thread_id}: Starting...")
        driver.get(url)

        handle_cookie_modal(driver, thread_id)

        # Extract links
        links = extract_links(driver, thread_id, number_of_links)
        print(f"Thread-{thread_id}: Extracted {len(links)} links.")

        # Scrape articles
        for link in links:
            article_content = scrape_article(driver, thread_id, link)
            if article_content:
                results.append(article_content)
    finally:
        driver.quit()
        print(f"Thread-{thread_id}: Done.")

def scrape_dynamic_links_and_articles(url, total_links=20, num_threads=1):
    results = []
    threads = []
    links_per_thread = total_links // num_threads

    start_time = time.time()

    for thread_id in range(num_threads):
        thread = threading.Thread(
            target=scrape_links_and_articles, 
            args=(url, results, thread_id, service, options, links_per_thread)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Collected {len(results)} articles in {elapsed_time:.2f} seconds.")  
    return results

def check_if_article_requires_subscription(driver, thread_id, link):
    publishers = driver.find_element((By.CLASS_NAME, "publishing yf-1weyqlp"))
    
    #Also iterate though all of the items 
    #Have a list of predefined publishers that require subsriptions example below dict
    publishers_w_subscriptions = {}
    for publisher in publishers:
        if publisher in publishers_w_subscriptions:
            return

# Example 
if __name__ == "__main__":
    url = "https://finance.yahoo.com/quote/TSLA/news/"
    articles = scrape_dynamic_links_and_articles(url, total_links=10, num_threads=2)
    print(articles)
