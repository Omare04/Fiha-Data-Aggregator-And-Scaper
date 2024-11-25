from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

options = Options()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')
service = Service('/usr/local/bin/chromedriver')

def scrape_links_and_articles(url, results, thread_id, number_of_links=10):
    driver = webdriver.Chrome(service=service, options=options)
    try:
        print(f"Thread-{thread_id}: Starting...")
        driver.get(url)

        # Handle cookie modal
        try:
            reject_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "reject-all"))
            )
            reject_button.click()
        except Exception:
            print(f"Thread-{thread_id}: No cookie modal.")

        # Extract links
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
            time.sleep(1)  # Rate limiting to avoid server overload

        # Scrape articles
        for link in links:
            try:
                driver.get(link)
                article_content = ""

                # Handle "Story continues" button
                try:
                    story_continues_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "secondary-btn.fin-size-large.readmore-button.rounded.yf-15mk0m"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", story_continues_button)
                    
                    # Try clicking using JavaScript if direct click fails
                    try:
                        story_continues_button.click()
                        print(f"Thread-{thread_id}: 'Story continues' button clicked for {link}.")
                    except Exception as e:
                        print(f"Thread-{thread_id}: Direct click failed, using JavaScript for {link}. {e}")
                        driver.execute_script("arguments[0].click();", story_continues_button)

                except Exception as e:
                    print(f"Thread-{thread_id}: No 'Story continues' button for {link}: {e}")

                # Extract all visible paragraphs
                paragraphs = driver.find_elements(By.CLASS_NAME, "yf-1pe5jgt")
                for paragraph in paragraphs:
                    article_content += paragraph.text.strip() + " "

                if article_content.strip():
                    results.append(article_content.strip())
                else:
                    print(f"Thread-{thread_id}: No content found for {link}.")

            except Exception as e:
                print(f"Thread-{thread_id}: Error scraping article at {link}: {e}")
    finally:
        driver.quit()
        print(f"Thread-{thread_id}: Done.")


def scrape_dynamic_links_and_articles(url, total_links=20, num_threads=1):
    results = []
    threads = []
    links_per_thread = total_links // num_threads
    
    start_time = time.time()

    for thread_id in range(num_threads):
        thread = threading.Thread(target=scrape_links_and_articles, args=(url, results, thread_id, links_per_thread))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"Collected {len(results)} articles in {elapsed_time:.2f} seconds.")  
    return results

# Example 
url = "https://finance.yahoo.com/quote/AAPL/news/"
articles = scrape_dynamic_links_and_articles(url, total_links=5, num_threads=2)
print(articles)
