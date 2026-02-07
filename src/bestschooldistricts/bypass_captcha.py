from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up ChromeDriver path
chromedriver_path = "/opt/homebrew/bin/chromedriver"  # Adjust to your path
service = Service(chromedriver_path)

# Initialize WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Target URL
url = "https://www.niche.com/k12/d/adlai-e-stevenson-high-school-district-no-125-il/"

try:
    # Open the webpage
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Locate the "Press and Hold" button
    button = driver.find_element(By.CSS_SELECTOR, "div#px-captcha")  # Adjust the selector if needed

    # Simulate "press and hold"
    print("Pressing and holding the button...")
    action = ActionChains(driver)
    action.click_and_hold(button).perform()

    # Hold the button for 15 seconds
    time.sleep(15)  # Adjust this duration if needed
    action.release(button).perform()
    print("Released the button.")

    # Wait for CAPTCHA to process
    time.sleep(5)

    # Save the page after solving CAPTCHA
    html = driver.page_source
    with open("data/html_pages/solved_page.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("CAPTCHA solved and page saved successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()
