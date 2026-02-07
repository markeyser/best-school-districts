from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to ChromeDriver
chromedriver_path = "/opt/homebrew/Caskroom/chromedriver/132.0.6834.110/chromedriver-mac-x64/chromedriver"

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Test: Open a webpage
try:
    driver.get("https://www.google.com")
    print(f"Page title: {driver.title}")
finally:
    driver.quit()
