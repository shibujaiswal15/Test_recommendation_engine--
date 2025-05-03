from difflib import SequenceMatcher
  # Make sure you have this function implemented
import json
import os
from utils.extractor import extract_constraints


# Load your scraped assessment data (adjust the path if needed)
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'final_data.json')

# Normalize the path
file_path = os.path.normpath(file_path)


with open(file_path, encoding='utf-8') as f:

    shl_data = json.load(f)

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# --- Improved Scoring Function ---
def match_score(test, constraints):
    score = 0
    reasons = []

    description = test.get("description", "").lower()
    title = test.get("name", "").lower()
    keywords = test.get("keywords", [])
    all_text = " ".join([description, title] + keywords).lower()

    # Skills
    for skill in constraints.get("skills", []):
        if any(similarity(skill, kw) > 0.7 for kw in keywords) or skill.lower() in all_text:
            score += 1
            reasons.append(f"Skill matched: {skill}")

    # Job level
    job_level = constraints.get("job_level", "").lower()
    test_levels = [lvl.lower() for lvl in test.get("job_levels", [])]
    if job_level in test_levels or "all" in test_levels:
        score += 1
        reasons.append("Job level matched")

    # Duration
    try:
        test_duration = int(test.get("assessment_length", 999))
        if test_duration <= constraints.get("duration_limit", 999):
            score += 1
            reasons.append("Duration matched")
    except:
        pass

    # Assessment type keys
    constraint_keys = constraints.get("assessment_types", [])
    test_keys = test.get("keys", [])
    match_count = sum(1 for k in constraint_keys if k in test_keys)
    if match_count:
        score += match_count
        reasons.append(f"Matched {match_count} assessment type(s)")

    return score


# --- Recommender Function ---
def recommend_tests(prompt: str, top_k: int = 10):
    constraints = extract_constraints(prompt)
    print("\nExtracted Constraints:", constraints)

    if not constraints:
        print("Could not extract constraints from prompt.")
        return []

    scored = []
    for test in shl_data:
        score = match_score(test, constraints)
        scored.append((score, test))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:top_k]