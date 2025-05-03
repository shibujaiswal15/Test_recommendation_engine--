import json

original_file = "final1.json"         # Full data
correct_flags_file = "shl_tests.json" # Has correct values

# Load both
with open(original_file, "r", encoding="utf-8") as f1:
    full_data = json.load(f1)

with open(correct_flags_file, "r", encoding="utf-8") as f2:
    flag_data = json.load(f2)

# Map link to flags
flag_lookup = {entry["link"]: entry for entry in flag_data}

updated_count = 0
not_found = 0

for entry in full_data:
    link = entry.get("link")
    if link in flag_lookup:
        flags = flag_lookup[link]
        entry["remote_available"] = flags.get("remote_available", "No")
        entry["adaptive_irt"] = flags.get("adaptive_available", "No")
        updated_count += 1
    else:
        not_found += 1
        print(f"⚠️ No match found for: {entry.get('name')}")

# Save
with open("shl_tests_updated.json", "w", encoding="utf-8") as f_out:
    json.dump(full_data, f_out, indent=2, ensure_ascii=False)

print(f"\n✅ Updated {updated_count} entries.")
print(f"❌ No match for {not_found} entries.")
