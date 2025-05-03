from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json, time

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def load_and_deduplicate(filepath="test.json"):
    with open(filepath, "r") as f:
        tests = json.load(f)

    # Deduplicate based on 'link'
    seen_links = set()
    unique_tests = []
    for test in tests:
        link = test.get("link")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_tests.append(test)

    print(f"🧹 Deduplicated: {len(tests) - len(unique_tests)} removed, {len(unique_tests)} remaining.")
    return unique_tests

def extract_flags_from_table(soup):
    row = soup.select_one('tr[data-entity-id]')
    if not row:
        return "No", "No"  # Default fallback

    tds = row.select('td.custom__table-heading__general')
    
    if len(tds) < 2:
        return "No", "No"

    remote_available = "Yes" if tds[0].select_one('catalogue__circle -yes') else "No"
    adaptive_irt = "Yes" if tds[1].select_one('catalogue__circle -yes') else "No"

    return remote_available, adaptive_irt

def fix_flags_in_tests(filepath="test.json"):
    tests = load_and_deduplicate(filepath)
    driver = setup_driver()
    updated_count = 0

    for test in tests:
        if test.get("flags_fixed"):  # Skip if already fixed
            continue

        try:
            driver.get(test["link"])
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # ✅ Use updated logic
            remote, adaptive = extract_flags_from_table(soup)
            test["remote_available"] = remote
            test["adaptive_irt"] = adaptive
            test["flags_fixed"] = True

            updated_count += 1
            print(f"✅ Updated: {test['name']}")

        except Exception as e:
            print(f"⚠️ Failed: {test.get('name', 'Unknown')}, Error: {e}")

    driver.quit()

    # Reassign serial numbers
    for i, test in enumerate(tests, start=1):
        test["s_no"] = i

    with open(filepath, "w") as f:
        json.dump(tests, f, indent=2)

    print(f"\n🛠️ Flags fixed for {updated_count} test(s). Saved {len(tests)} unique test(s).")

# Run
if __name__ == "__main__":
    fix_flags_in_tests()
