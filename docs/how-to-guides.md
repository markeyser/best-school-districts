# Installing ChromeDriver on MacBook Pro M1: A Step-by-Step Guide

This guide explains how to successfully install and configure ChromeDriver on a MacBook Pro M1 using Poetry for managing Python dependencies.

---

## Prerequisites
1. **Poetry** installed:
   ```bash
   pip install poetry
   ```
2. **Selenium Python Library** added to your project:
   ```bash
   poetry add selenium
   ```
3. **Python** installed and accessible (e.g., Python 3.9+).
4. **Homebrew** installed on your system (optional).

---

## Steps to Install and Configure ChromeDriver

### 1. Download ChromeDriver
- Open the **[ChromeDriver download page](https://googlechromelabs.github.io/chrome-for-testing/)**.
- Select the version matching your **Google Chrome** browser version (check it in `chrome://settings/help`).
- Download the **mac-arm64** version for M1 chips.

Alternatively, install ChromeDriver via Homebrew:
```bash
brew install --cask chromedriver
```

---

### 2. Locate ChromeDriver
If you used Homebrew, ChromeDriver is located at:
```
/opt/homebrew/bin/chromedriver
```

---

### 3. Grant Permissions to ChromeDriver
macOS blocks apps from unidentified developers by default. Follow these steps:

1. **Grant Full Disk Access:**
   - Open **Settings** > **Privacy & Security** > **Full Disk Access**.
   - Add **iTerm** and **Terminal** to the list of apps with access.

2. **Remove the Quarantine Attribute:**
   Run the following command in your terminal:
   ```bash
   sudo xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
   ```

3. **Manually Open ChromeDriver:**
   - Navigate to `/opt/homebrew/bin`.
   - Open the `chromedriver` file manually by double-clicking it.
   - You should see the following output in your terminal:
     ```
     Last login: Mon Jan 27 10:34:50 on ttys000
     /opt/homebrew/bin/chromedriver ; exit;
     [oh-my-zsh] It's time to update! You can do that by running `omz update`
     (base) markeyser@Marcoss-MBP ~ /opt/homebrew/bin/chromedriver ; exit;
     Starting ChromeDriver 132.0.6834.110 (df453a35f099772fdb954e33551388add2ca3cde-refs/branch-heads/6834_101@{#3}) on port 0
     Only local connections are allowed.
     ```

---

### 4. Verify ChromeDriver Installation
Check if ChromeDriver is working by running:
```bash
/opt/homebrew/bin/chromedriver --version
```
Expected output:
```
 --version
ChromeDriver 132.0.6834.110 (df453a35f099772fdb954e33551388add2ca3cde-refs/branch-heads/6834_101@{#3})
```

---

### 5. Integrate ChromeDriver with Selenium in Poetry
Create a script to test the installation. Save the following as `src/bestschooldistricts/test_chromedriver.py`:
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to ChromeDriver
chromedriver_path = "/opt/homebrew/bin/chromedriver"

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
```

Run the script:
```bash
poetry run python src/bestschooldistricts/test_chromedriver.py
```

Expected output:
```
Page title: Google
```

---

## Troubleshooting
### If You Encounter Issues:
1. **Quarantine Issues:**
   - Ensure the `com.apple.quarantine` attribute has been removed:
     ```bash
     sudo xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
     ```

2. **Permissions:**
   - Verify that Full Disk Access has been granted to your terminal application.

3. **Version Mismatch:**
   - Ensure ChromeDriver matches the version of your installed Google Chrome.

---

## Summary
By following these steps, you have successfully installed and configured ChromeDriver at `/opt/homebrew/bin/chromedriver` on your MacBook Pro M1. You are now ready to use Selenium with ChromeDriver for browser automation.
