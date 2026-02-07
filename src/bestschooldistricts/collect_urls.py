import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import random

# Base URLs
base_url = "https://www.niche.com/k12/search/best-school-districts/"
paged_url = "https://www.niche.com/k12/search/best-school-districts/?page={}"

# Create a fake user agent
ua = UserAgent()

# Data storage
district_urls = []

# Loop through all 100 pages
for page in range(1, 101):  # Assuming 100 pages
    try:
        # Choose the correct URL
        url = base_url if page == 1 else paged_url.format(page)
        
        # Set headers to mimic a browser
        headers = {
            "User-Agent": ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }
        
        # Send the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all links to district pages
        links = soup.select("a.search-result__link")
        for link in links:
            district_url = "https://www.niche.com" + link["href"]
            district_urls.append(district_url)

        print(f"Scraped page {page}, found {len(links)} links.")
        
        # Add a delay to avoid getting blocked
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error scraping page {page}: {e}")

# Save URLs to a CSV
df = pd.DataFrame({"School District URL": district_urls})
df.to_csv("data/external/school_district_urls.csv", index=False)
print(f"Saved {len(district_urls)} district URLs to school_district_urls.csv.")
