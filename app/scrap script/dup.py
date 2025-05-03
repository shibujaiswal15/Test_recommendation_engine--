import json

input_file = "shl_tests.json"
output_file = "final1.json"

# Load the JSON data
with open(input_file, "r") as f:
    data = json.load(f)

# Use a set to track unique names
seen = set()
unique_data = []

for item in data:
    name = item["name"].strip()
    if name not in seen:
        seen.add(name)
        unique_data.append(item)

# Renumber s_no
for idx, item in enumerate(unique_data, 1):
    item["s_no"] = idx

# Save the cleaned list
with open(output_file, "w") as f:
    json.dump(unique_data, f, indent=2)

print(f"✅ Removed duplicates. {len(unique_data)} unique entries saved to '{output_file}'.")
