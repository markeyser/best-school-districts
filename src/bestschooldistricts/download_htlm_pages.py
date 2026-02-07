from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time
import pandas as pd
import random

# Path to ChromeDriver
chromedriver_path = "/opt/homebrew/bin/chromedriver"

# Load URLs from CSV
csv_path = "data/external/school_district_urls.csv"
districts = pd.read_csv(csv_path)

# Output directory for HTML pages
output_dir = "data/html_pages"
os.makedirs(output_dir, exist_ok=True)

# Set up Selenium WebDriver
service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Loop through URLs and download HTML
for idx, row in districts.iterrows():
    url = row["School District URL"]
    district_name = url.split("/")[-2]  # Use last part of the URL for naming
    output_file = os.path.join(output_dir, f"{district_name}.html")

    # Skip already downloaded pages
    if os.path.exists(output_file):
        print(f"Skipping {district_name}, already downloaded.")
        continue

    try:
        # Access the page
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Add random delay to avoid detection

        # Save the page source
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print(f"Downloaded: {district_name}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Quit the driver
driver.quit()
print(f"HTML pages saved to {output_dir}")
