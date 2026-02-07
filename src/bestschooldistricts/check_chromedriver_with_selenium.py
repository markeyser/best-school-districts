from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path to ChromeDriver
chromedriver_path = "/opt/homebrew/bin/chromedriver"

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (remove if you want to see the browser)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open a webpage
    driver.get("https://www.example.com")

    # Extract the title of the page
    page_title = driver.title
    print(f"Page Title: {page_title}")

    # Find elements (Example: headings)
    headings = driver.find_elements(By.TAG_NAME, "h1")
    for heading in headings:
        print(f"Heading: {heading.text}")

finally:
    # Quit the browser
    driver.quit()
