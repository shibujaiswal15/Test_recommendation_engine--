import json
import google.generativeai as genai
from difflib import SequenceMatcher
import os



with open("app/data/shl_tests_main.json", "r") as f:
    shl_data = json.load(f)

def extract_constraints(prompt: str):
    system_prompt = """
    You are an AI assistant helping recruiters match hiring needs to suitable assessments.

    Extract the following structured information from the prompt and output only in valid JSON format:

    {
      "skills": [list of mentioned skills like Python, Java, Communication],
      "job_level": one of ["Entry", "Mid", "Senior", "Executive", "Graduate", "All"],
      "duration_limit": integer (in minutes),
      "assessment_types": list of applicable test categories based on the prompt clues.
          Map them using:
            - "A" = Ability & Aptitude (Cognitive)
            - "B" = Biodata & Situational Judgement
            - "C" = Competencies
            - "D" = Development & 360
            - "E" = Assessment Exercises
            - "K" = Knowledge & Skills (Coding, Tech, Language)
            - "P" = Personality & Behavior
            - "S" = Simulations
      "language": language preference if mentioned, else null,
      "constraints": any additional instructions like "adaptive", "remote", etc.
    }

    Do not explain. Just return the JSON.
    """

    full_prompt = f"{system_prompt}\n\nPrompt:\n\"{prompt}\""

    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    try:
        response = model.generate_content(full_prompt)
        content = response.text.strip()
        if content.startswith("```json"):
            content = content.strip("```json").strip("```").strip()
        elif content.startswith("```"):
            content = content.strip("```").strip()

        
        parsed = json.loads(content)
        return parsed
    except json.JSONDecodeError:
        print("[Gemini] ❌ Failed to parse JSON from response:")
        print(response.text)
        return None
    except Exception as e:
        print(f"[Gemini] ❌ Unexpected error: {e}")
        return None

# --- Utility ---
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

# --- CLI Interface ---
if __name__ == "__main__":
    user_prompt = input("Enter your hiring needs: ")
    top_matches = recommend_tests(user_prompt)

    # print("\nTop Matching Assessments:\n")
    # for score, test in top_matches:
    #     print(f"{test['name']} ({test.get('assessment_length', 'Unknown')} mins, Score: {score}) -> {test.get('link', 'N/A')}")

    print("\nTop Matching Assessments:\n")
    for score, test in top_matches:
        name = test.get("name", "Unnamed")
        link = test.get("link", "#")
        duration = test.get("assessment_length", "N/A")
        test_types = test.get("keys", [])
        remote = "✅ Yes" if test.get("is_remote", False) else "❌ No"
        adaptive = "✅ Yes" if test.get("is_adaptive", False) else "❌ No"
        job_levels = ", ".join(test.get("job_levels", []))
        description = test.get("description", "No description available.")

        # You can map keys to their meanings if needed
        key_map = {
            "A": "Ability & Aptitude",
            "B": "Biodata & Situational Judgement",
            "C": "Competencies",
            "D": "Development & 360",
            "E": "Assessment Exercises",
            "K": "Knowledge & Skills",
            "P": "Personality & Behavior",
            "S": "Simulations"
        }
        test_types_verbose = [f"{key_map.get(k, k)} ({k})" for k in test_types]

        print(f"📌 Assessment Name: {name} ({', '.join(test_types)})")
        print(f"🔗 Link: {link}")
        print(f"🕒 Duration: {duration} minutes")
        print(f"🧠 Type: {', '.join(test_types_verbose)}")
        print(f"🌐 Remote Testing: {remote}")
        print(f"📈 Adaptive/IRT Support: {adaptive}")
        print(f"🎯 Target Job Levels: {job_levels}")
        # print(f"📋 Description: {description}")
        print("-" * 80)
