import time
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urls = [
    "https://www.shl.com/solutions/products/product-catalog/?start=12&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=24&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=36&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=48&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=60&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=72&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=84&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=96&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=108&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=120&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=132&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=144&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=156&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=168&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=180&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=192&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=204&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=216&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=228&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=240&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=252&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=264&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=276&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=288&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=300&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=312&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=324&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=336&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=348&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=360&type=1&type=1",
    "https://www.shl.com/solutions/products/product-catalog/?start=372&type=1&type=1"
]

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def parse_test_row(tr):
    title_cell = tr.select_one("td.custom__table-heading__title a")
    if not title_cell:
        raise ValueError("Missing title cell")

    name = title_cell.text.strip()
    link = "https://www.shl.com" + title_cell['href']

    general_cells = tr.select("td.custom__table-heading__general")
    remote_available = "Yes" if general_cells and general_cells[0].find("span") else "No"
    adaptive_available = "Yes" if len(general_cells) > 1 and general_cells[1].find("span") else "No"

    return {
        "name": name,
        "link": link,
        "remote_available": remote_available,
        "adaptive_available": adaptive_available
    }

def load_existing_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def scrape_urls(urls, json_file="shl_tests.json"):
    driver = setup_driver()
    all_tests = load_existing_json(json_file)

    existing_links = {test["link"] for test in all_tests}

    for url in urls:
        print(f"🔄 Scraping: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )
        except Exception as e:
            print(f"❌ Timeout or error loading page: {e}")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        test_rows = soup.select("table tbody tr")

        if not test_rows:
            print("⚠️ No test rows found on page.")
            continue

        new_tests = 0
        for tr in test_rows:
            try:
                test_info = parse_test_row(tr)
                if test_info["link"] not in existing_links:
                    all_tests.append(test_info)
                    existing_links.add(test_info["link"])
                    new_tests += 1
            except Exception as e:
                print(f"⚠️ Skipping row due to error: {e}")
                continue

        print(f"✅ Added {new_tests} new test(s) from current page.")

    driver.quit()

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(all_tests, f, indent=2, ensure_ascii=False)

    print(f"📦 Updated {json_file} with total {len(all_tests)} tests.")

if __name__ == "__main__":
    scrape_urls(urls)