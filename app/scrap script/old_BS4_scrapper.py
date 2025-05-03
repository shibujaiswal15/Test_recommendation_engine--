import requests
import json
from bs4 import BeautifulSoup

# List of URLs to scrape
urls = [
    # "https://www.shl.com/solutions/products/product-catalog/?start=0&type=1&type=1",
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

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to scrape data
def scrape_shl_catalog():
    all_tests = []
    serial_number = 1  # Start serial numbering from 1

    for url in urls:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"❌ Failed to load {url}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all test entries
        test_rows = soup.find_all("tr", {"data-course-id": True})

        for row in test_rows:
            test_data = {"s_no": serial_number}  # Add serial number

            # Extract test name and link
            title_tag = row.find("td", class_="custom__table-heading__title")
            if title_tag and title_tag.a:
                test_data["name"] = title_tag.a.text.strip()
                test_data["link"] = "https://www.shl.com" + title_tag.a["href"]

            # Extract Remote and Adaptive/IRT availability
            general_tags = row.find_all("td", class_="custom__table-heading__general")
            if len(general_tags) >= 2:
                test_data["remote_available"] = "Yes" if general_tags[0].find(class_="catalogue-cricle_yes") else "No"
                test_data["adaptive_irt"] = "Yes" if general_tags[1].find(class_="catalogue-cricle_yes") else "No"

            # Extract product catalogue keys
            key_container = row.find("td", class_="custom__table-heading__general product-catalogue__keys")
            if key_container:
                test_data["keys"] = [key.text.strip() for key in key_container.find_all("span", class_="product-catalogue__key")]

            all_tests.append(test_data)
            serial_number += 1  # Increment serial number

    # Save results to JSON
    with open("shl_tests.json", "w") as f:
        json.dump(all_tests, f, indent=2)

    print(f"✅ Scraped {len(all_tests)} tests and saved to shl_tests.json")

# Run scraper
if __name__ == "__main__":
    scrape_shl_catalog()