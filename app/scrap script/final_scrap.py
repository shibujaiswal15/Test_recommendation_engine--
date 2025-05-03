import requests
import json
import os
from bs4 import BeautifulSoup
import re

# Define file path
json_file_path = os.path.join("final1.json")

# Load JSON data
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

scraped_data = []

for item in data:
    url = item.get("link", "")
    if not url:
        continue

    print(f"Scraping: {url}")

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting description
        description_section = soup.select_one(".product-catalogue-training-calendar__row")
        description = description_section.get_text(strip=True) if description_section else "-1"

        # Extracting job levels
        job_levels_section = soup.select_one(".product-catalogue-training-calendar__row:nth-of-type(2)")
        job_levels = [job.strip() for job in job_levels_section.get_text(strip=True).split(",")] if job_levels_section else []

        # Extracting languages
        languages_section = soup.select_one(".product-catalogue-training-calendar__row:nth-of-type(3)")
        languages = [lang.strip() for lang in languages_section.get_text(strip=True).split(",")] if languages_section else []

        # Extracting assessment length
        # assessment_section = soup.select_one(".product-catalogue-training-calendar__row:nth-of-type(4)")
        # assessment_text = assessment_section.get_text(strip=True) if assessment_section else "-1"
        # assessment_length = int(assessment_text.split("=")[-1].strip()) if "=" in assessment_text else "-1"

        # Extracting assessment length
        assessment_section = soup.select_one(".product-catalogue-training-calendar__row:nth-of-type(4)")
        assessment_text = assessment_section.get_text(strip=True) if assessment_section else "-1"

        # Use regex to safely extract only the first number from the text
        match = re.search(r'\d+', assessment_text)
        assessment_length = int(match.group()) if match else -1

        # Construct final structured data
        final_entry = {
            **item,  # Preserve existing data
            "description": description,
            "job_levels": job_levels,
            "languages": languages,
            "assessment_length": assessment_length
        }

        scraped_data.append(final_entry)

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")

# Save updated JSON file
with open(json_file_path, "w", encoding="utf-8") as file:
    json.dump(scraped_data, file, indent=4, ensure_ascii=False)

print("Scraping completed. Data saved to shl_tests_main.json")
