import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

JSON_FILE = "shl_tests.json"

# Load existing data if file exists
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        all_tests = json.load(f)
else:
    all_tests = []

# Track existing names or links to avoid duplicates
existing_links = {test["link"] for test in all_tests}
serial = len(all_tests) + 1

def fetch_page(start):
    url = f"{BASE_URL}?start={start}&type=1&type=1"
    print(f"Fetching: {url}")
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def extract_tests(soup, serial):
    rows = soup.select("tr[data-entity-id]")
    tests = []

    for row in rows:
        a_tag = row.select_one("td.custom__table-heading__title a")
        if not a_tag:
            continue

        link = "https://www.shl.com" + a_tag["href"]
        if link in existing_links:
            continue  # skip already recorded tests

        test = {
            "s_no": serial,
            "name": a_tag.text.strip(),
            "link": link
        }
        serial += 1

        general_cells = row.select("td.custom__table-heading__general")
        test["remote_available"] = "Yes" if general_cells and general_cells[0].select_one(".catalogue_cricle_yes") else "No"
        test["adaptive_irt"] = "Yes" if len(general_cells) > 1 and general_cells[1].select_one(".catalogue_cricle_yes") else "No"

        key_cells = row.select("td.product-catalogue__keys span.product-catalogue__key")
        test["keys"] = [span.text.strip() for span in key_cells]

        tests.append(test)
        existing_links.add(link)

    return tests, serial

# Scrape and append new entries
start = 12
while True:
    soup = fetch_page(start)
    tests, serial = extract_tests(soup, serial)
    if not soup.select("tr[data-entity-id]"):
        break
    all_tests.extend(tests)
    start += 12

# Save combined data
with open(JSON_FILE, "w") as f:
    json.dump(all_tests, f, indent=2)

print(f"✅ Done. Total unique tests: {len(all_tests)}")
