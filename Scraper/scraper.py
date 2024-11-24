from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

# Function to scrape links using Selenium
def scrape_links_in_thread(url, results, thread_id, number_of_links=20):
    options = Options()
    # options.add_argument('--headless')  # Remove if you want to see the UI
    options.add_argument('--disable-gpu')
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Thread-{thread_id}: Starting...")
        driver.get(url)
        time.sleep(3)  # Allow time for the initial page to load

        # Handle the cookie consent modal
        try:
            reject_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "reject-all"))
            )
            reject_button.click()
            print(f"Thread-{thread_id}: Cookie consent rejected.")
        except Exception as e:
            print(f"Thread-{thread_id}: No cookie consent modal or issue handling it: {e}")

        # Scroll to load more content
        links = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        while len(links) < number_of_links:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for content to load

            # Extract links
            try:
                anchors = driver.find_elements(By.CSS_SELECTOR, "a.subtle-link.fin-size-small.thumb")
                for anchor in anchors:
                    href = anchor.get_attribute("href")
                    if href and href not in links:
                        links.append(href)
                    if len(links) >= number_of_links:
                        break
            except Exception as e:
                print(f"Thread-{thread_id}: Error extracting links: {e}")
                break

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Append results to shared list
        results.extend(links)
        print(f"Thread-{thread_id}: Found {len(links)} links.")

    finally:
        driver.quit()
        print(f"Thread-{thread_id}: Done.")

# Multithreaded function to scrape links
def scrape_dynamic_links_multithreaded(url, total_links=100, num_threads=2):
    start_time = time.time()

    # Calculate the number of links per thread
    links_per_thread = total_links // num_threads

    # Shared list to store results
    results = []

    # List to keep track of threads
    threads = []

    # Start threads
    for thread_id in range(num_threads):
        thread = threading.Thread(
            target=scrape_links_in_thread,
            args=(url, results, thread_id, links_per_thread)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()
    duration = end_time - start_time
    print(f"Scraping completed in {duration:.2f} seconds with {num_threads} threads.")
    print(f"Total links collected: {len(results)}")
    return results

# Example usage
url = "https://finance.yahoo.com/quote/TSLA/news/"
dynamic_links = scrape_dynamic_links_multithreaded(url, total_links=100, num_threads=2)

if dynamic_links:
    print(f"Found a total of {len(dynamic_links)} links.")
    for i, link in enumerate(dynamic_links, 1):
        print(f"{i}: {link}")
else:
    print("No links found.")



#Now you need to retrieve the articles content
#Make sure to account for "continue reading" articles with an if statement in the article scraper
#Then clean the data and pipe it to a mongo db, by adding it to its associated stock object and adding 
#When the article was released