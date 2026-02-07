# Web Scraping NICHE - 2025 Best School Districts in America

Location of the data data:

- [2025 Best School Districts in America](https://www.niche.com/k12/search/best-school-districts/?utm_source=chatgpt.com)

## Web scraping the data

### Collecting the URLs

Get the URL of each of the top 100 out of more than 400 school
districts listed in "2025 Best School Districts in America".

- `src/bestschooldistricts/collect_urls.py`

The 100 URLs has been saved here:

- `data/external/school_district_urls.csv`

First lines of the file:

```text
School District URL
https://www.niche.com/k12/d/adlai-e-stevenson-high-school-district-no-125-il/
https://www.niche.com/k12/d/glenbrook-high-school-district-225-il/
```

### Download the HTML web pages

I installed fist `chromedrvier` following these instructions:

- `docs/how-to-guides.md`

Then, I checked that `crhomedriver` works as expected:

- `src/bestschooldistricts/check_chromedriver_with_selenium.py`

Then, I downloaded the 100 HTLM pages for each of the 100 URLs in the
CSV file.

The downloaded HTLM pages are here:

- `data/html_pages`

### Parsing the HTML pages

Now, we extract from the HTML pages the fields we are interested on:

- School District Name: `Pleasanton Unified School District`
- Overall Ranking: Based on the position on the CSV file.
- Overall Grade: `A+`
- School District Location: `PLEASANTON, CA`
- Median Household Income: `$226,870`
- Median Rent: `$2,763`
- Median Home Value: `$1,659,299`

We send the data to a CSV file.

--

$1,336,500
BETHPAGE, NY $597,400
CARMEL, CA $723,100
PLEASANTON, CA $1,659,299
LA CANADA, CA $2,000,001
BRONXVILLE, NY $1,137,700
SAN MATEO, CA $1,563,200
SOUTHLAKE, TX $957,500
CINCINNATI, OH $584,400
MILLBURN, NJ $1,318,800
NORTHFIELD, IL $807,
GRAPEVINE, TX $470,400
COPPELL, TX $525,300
