import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
api= os.getenv("GEMINI_API_KEY")
genai.configure(api_key = api)

# genai.configure(api_key)


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
