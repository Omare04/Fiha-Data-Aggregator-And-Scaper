from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_dynamic_links(url):
    # Set up Selenium WebDriver
    options = Options()
    # Remove headless to see the UI, good for debugging
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    start_time = time.time()

    try:
        driver.get(url)
        time.sleep(3)  # Allow time for the initial page to load

        # Handle the cookie consent modal
        try:
            # Wait for the "Reject all" button and click it
            reject_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "reject-all"))  # Using the class name
            )
            reject_button.click()
            print("Cookie consent rejected.")
        except Exception as e:
            print("No cookie consent modal found or issue handling it:", e)

        # Scroll to load more content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for content to load

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Wait for <a> elements with specific class to load
        try:
            anchors = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a.subtle-link.fin-size-small.thumb")
                )
            )
        except Exception as e:
            print(f"Error locating elements: {e}")
            return []

        # Extract links
        links = []
        number_of_links = 100
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if href and href not in links:
                links.append(href)
            if len(links) >= number_of_links:  
                break
            
        end_time = time.time()
        duration = end_time - start_time
        print(f"It took {duration:.2f} seconds to scrape {number_of_links} links.")

        return links

    finally:
        driver.quit()

# Example usage
url = "https://finance.yahoo.com/quote/TSLA/news/"
dynamic_links = scrape_dynamic_links(url)

if dynamic_links:
    print(f"Found a total of {len(dynamic_links)} links.")
    for i, link in enumerate(dynamic_links, 1):
        print(f"{i}: {link}")
else:
    print("No links found.")
