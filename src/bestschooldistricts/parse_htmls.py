from bs4 import BeautifulSoup
import os
import pandas as pd

# Directory containing downloaded HTML files
html_dir = "data/html_pages"

# Data storage
data = []

# Loop through all HTML files
for file_name in os.listdir(html_dir):
    file_path = os.path.join(html_dir, file_name)
    try:
        # Open and parse the HTML file
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Check if the page is a CAPTCHA page
        if "Access to this page has been denied" in soup.text:
            print(f"CAPTCHA encountered in file: {file_name}")
            continue

        # Extract data
        district_name = soup.find("h1", class_="postcard__title").text.strip()
        overall_grade = soup.find("div", class_="postcard__badge").text.strip()
        location = soup.find("div", class_="postcard__attr").text.strip()

        # Extract median household income, rent, and home value
        income_element = soup.find(text="Median Household Income")
        rent_element = soup.find(text="Median Rent")
        home_value_element = soup.find(text="Median Home Value")

        income = income_element.find_next("div").text.strip() if income_element else "N/A"
        rent = rent_element.find_next("div").text.strip() if rent_element else "N/A"
        home_value = home_value_element.find_next("div").text.strip() if home_value_element else "N/A"

        # Add extracted data to the list
        data.append({
            "School District Name": district_name,
            "Overall Grade": overall_grade,
            "School District Location": location,
            "Median Household Income": income,
            "Median Rent": rent,
            "Median Home Value": home_value,
        })

        print(f"Scraped: {district_name}")

    except Exception as e:
        print(f"Failed to process {file_name}: {e}")

# Save the data to a CSV file
output_csv = "data/processed/school_district_data.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)
print(f"Data saved to {output_csv}")
