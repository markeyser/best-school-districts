import csv
import time
import random
import requests
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import undetected_chromedriver as uc

# === CONFIGURATION ===
chromedriver_path = "/opt/homebrew/bin/chromedriver"  # Update if necessary
url = "https://www.niche.com/k12/d/florence-city-schools-al/"

# === PROXY POOL ===
proxy_list = [
    "spkcqr8qpl:hxAHm71fw34tPn=juZ@gate.smartproxy.com:10001",
    "spkcqr8qpl:hxAHm71fw34tPn=juZ@gate.smartproxy.com:10002",
    "spkcqr8qpl:hxAHm71fw34tPn=juZ@gate.smartproxy.com:10003",
    # Add more proxies as needed
]

# === USER AGENT GENERATOR ===
ua = UserAgent()

# === LOGGING CONFIGURATION ===
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# === PROXY VALIDATION FUNCTION ===
def validate_proxy(proxy):
    try:
        response = requests.get("https://www.google.com", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
        if response.status_code == 200:
            logging.info(f"Proxy validated: {proxy}")
            return True
    except Exception as e:
        logging.error(f"Proxy validation failed for {proxy}: {e}")
    return False

# === GET WORKING PROXY FUNCTION ===
def get_working_proxy(proxy_list):
    random.shuffle(proxy_list)  # Shuffle to ensure random selection
    for proxy in proxy_list:
        if validate_proxy(proxy):
            logging.info(f"Using proxy: {proxy}")
            return proxy
        else:
            logging.warning(f"Proxy failed: {proxy}")
    raise Exception("No working proxies available.")

# === SELENIUM DRIVER CREATION ===
def create_driver(proxy=None):
    chrome_options = uc.ChromeOptions()
    
    # Random User-Agent
    user_agent = ua.random
    chrome_options.add_argument(f"user-agent={user_agent}")
    logging.info(f"Using User-Agent: {user_agent}")
    
    # Disable automation flags
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    
    # Set proxy if provided
    if proxy:
        chrome_options.add_argument(f"--proxy-server=http://{proxy}")
        logging.info(f"Configured proxy: {proxy}")
    
    # Optional: Headless mode (not recommended for CAPTCHA bypass)
    # chrome_options.add_argument("--headless")
    
    # Initialize undetected ChromeDriver
    try:
        driver = uc.Chrome(options=chrome_options, driver_executable_path=chromedriver_path)
        logging.info("ChromeDriver initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        raise e
    return driver

# === MAIN SCRAPING FUNCTION ===
def scrape_niche_page(url, proxy=None):
    driver = create_driver(proxy)
    try:
        # Step 1: Open URL
        driver.get(url)
        logging.info(f"Opened URL: {url} with proxy: {proxy}")
        time.sleep(5)  # Initial wait for page load

        # Step 2: Check for CAPTCHA presence
        try:
            captcha_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Press & Hold')]")
            logging.info("CAPTCHA detected. Attempting to bypass...")
    
            # Step 3: Hold the CAPTCHA button for 35 seconds
            action = ActionChains(driver)
            action.click_and_hold(captcha_button).perform()
            logging.info("Holding CAPTCHA button...")
            time.sleep(35)  # Hold the button for required duration
            action.release().perform()
            logging.info("CAPTCHA bypassed!")
    
            # Step 4: Wait for main content to load after CAPTCHA
            time.sleep(5)  # Adjust if necessary
        except Exception as captcha_e:
            logging.warning("No CAPTCHA detected or failed to locate CAPTCHA button.")
            logging.warning(f"CAPTCHA error: {captcha_e}")
    
        # Step 5: Verify page content by checking for a key element
        try:
            district_name = driver.find_element(By.CLASS_NAME, "postcard__title").text
            logging.info(f"District Name: {district_name}")
        except Exception as e:
            logging.error("Failed to find key element after CAPTCHA bypass.")
            logging.error(f"Element error: {e}")
            return  # Exit the function as essential data is missing
    
        # Step 6: Extract additional fields
        try:
            overall_grade = driver.find_element(By.CLASS_NAME, "postcard__badge").text
            location = driver.find_element(By.CLASS_NAME, "postcard__attr").text
            income = driver.find_element(By.XPATH, "//div[text()='Median Household Income']/following-sibling::div").text
            rent = driver.find_element(By.XPATH, "//div[text()='Median Rent']/following-sibling::div").text
            home_value = driver.find_element(By.XPATH, "//div[text()='Median Home Value']/following-sibling::div").text
    
            # Optionally, handle additional sections (e.g., "Read More About the Students")
            # Example: Click on the link and extract further data
            try:
                read_more_link = driver.find_element(By.LINK_TEXT, "Read More About the Students")
                read_more_link.click()
                logging.info("Clicked on 'Read More About the Students' link.")
                time.sleep(5)  # Wait for the new section to load
    
                # Extract additional student-related fields
                student_count = driver.find_element(By.XPATH, "//div[contains(text(),'Students')]/following-sibling::div").text
                diversity = driver.find_element(By.XPATH, "//div[contains(text(),'Diversity')]/following-sibling::div").text
    
                # Add to the extracted data
                data.update({
                    "Student Count": student_count,
                    "Diversity": diversity
                })
                logging.info("Extracted additional student-related fields.")
            except Exception as e:
                logging.warning("Failed to extract 'Read More About the Students' section.")
                logging.warning(f"Section error: {e}")
    
        except Exception as e:
            logging.error("Failed to extract additional fields.")
            logging.error(f"Extraction error: {e}")
            return  # Exit the function as essential data is missing
    
        # Step 7: Compile data
        data = {
            "School District Name": district_name,
            "Overall Grade": overall_grade,
            "Location": location,
            "Median Household Income": income,
            "Median Rent": rent,
            "Median Home Value": home_value,
            # Add more fields as needed
        }
    
        logging.info(f"Scraped data: {data}")
    
        # Step 8: Save data to CSV
        csv_file = "school_district_data.csv"
        try:
            # Write headers and data to CSV
            with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                # Write header only once
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)
            logging.info(f"Data saved to {csv_file}")
        except Exception as e:
            logging.error(f"Failed to save data to CSV: {e}")
    
    except Exception as e:
        logging.error(f"Error during scraping: {e}")
    finally:
        # Step 9: Save debug information
        try:
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            logging.info("Saved the current page source to debug_page.html.")
        except Exception as e:
            logging.error(f"Failed to save debug_page.html: {e}")
    
        driver.quit()

# === SCRIPT EXECUTION ===
if __name__ == "__main__":
    # Option 1: Single attempt with a working proxy
    try:
        proxy = get_working_proxy(proxy_list)
        scrape_niche_page(url, proxy)
    except Exception as e:
        logging.error(f"Failed to scrape with available proxies: {e}")
    
    # Option 2: Multiple attempts with different proxies
    # Uncomment the following block to enable multiple attempts
    
    # max_retries = len(proxy_list)
    # for attempt in range(max_retries):
    #     try:
    #         proxy = get_working_proxy(proxy_list)
    #         scrape_niche_page(url, proxy)
    #         break  # Exit loop if successful
    #     except Exception as e:
    #         logging.error(f"Attempt {attempt + 1} failed with proxy {proxy}: {e}")
    # else:
    #     logging.critical("All proxy attempts failed.")
