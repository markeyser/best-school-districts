import pandas as pd

# Load the CSV file
csv_path = "data/external/school_district_urls.csv"
districts = pd.read_csv(csv_path)

# Fix malformed URLs
districts["School District URL"] = districts["School District URL"].str.replace(
    r"https://www.niche.comhttps://www.niche.com", "https://www.niche.com", regex=False
)

# Save the corrected CSV
districts.to_csv(csv_path, index=False)
print(f"Fixed URLs saved to {csv_path}")
