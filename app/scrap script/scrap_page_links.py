from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json, os, time

urls = [
    "https://www.shl.com/solutions/products/product-catalog/?start=12&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=24&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=36&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=48&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=60&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=72&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=84&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=96&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=108&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=120&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=132&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=144&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=156&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=168&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=180&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=192&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=204&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=216&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=228&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=240&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=252&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=264&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=276&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=288&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=300&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=312&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=324&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=336&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=348&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=360&type=1&type=1",
    # "https://www.shl.com/solutions/products/product-catalog/?start=372&type=1&type=1"
]

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# def load_existing_tests(filepath="shl_tests.json"):
#     if os.path.exists(filepath):
#         with open(filepath, "r") as f:
#             return json.load(f)
#     return []

def scrape_shl_catalog():
    # existing_tests = load_existing_tests()
    # existing_links = {test.get("link") for test in existing_tests}

    all_tests = []
    new_count = 0

    driver = setup_driver()

    for url in urls:
        print(f"🔄 Scraping: {url}")
        driver.get(url)
        
        try:
             WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.product-catalogue"))
    )
        except:
            print(f"⚠️ Timeout waiting for test rows on {url}")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        test_rows = soup.find_all("tr", {"data-course-id": True})

        for row in test_rows:
            title_tag = row.find("td", class_="custom__table-heading__title")
            if not title_tag or not title_tag.a:
                continue

            test_name = title_tag.a.text.strip()
            test_link = "https://www.shl.com" + title_tag.a["href"]

            # if test_link in existing_links:
            #     continue

            test_data = {
                "s_no": len(all_tests) + 1,
                "name": test_name,
                "link": test_link
            }

            # Remote & Adaptive/IRT
            general_tags = row.find_all("td", class_="custom__table-heading__general")
            if len(general_tags) >= 2:
                test_data["remote_available"] = "Yes" if general_tags[0].find(class_="catalogue-cricle -yes") else "No"
                test_data["adaptive_irt"] = "Yes" if general_tags[1].find(class_="catalogue-cricle -yes") else "No"

            # Keys
            key_container = row.find("td", class_="custom__table-heading__general product-catalogue__keys")
            if key_container:
                test_data["keys"] = [key.text.strip() for key in key_container.find_all("span", class_="product-catalogue__key")]

            all_tests.append(test_data)
            # existing_links.add(test_link)
            new_count += 1

        time.sleep(2)  # Be kind to SHL servers

    driver.quit()

    # Update serial numbers
    for i, test in enumerate(all_tests, start=1):
        test["s_no"] = i

    with open("tests.json", "w") as f:
        json.dump(all_tests, f, indent=2)

    print(f"✅ Added {new_count} new test(s). Total tests: {len(all_tests)}")

# Run it
if __name__ == "__main__":
    scrape_shl_catalog()
