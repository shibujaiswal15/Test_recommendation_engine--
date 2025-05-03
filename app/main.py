from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Any
from utils.recommender import recommend_tests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # OR ["GET", "POST", "OPTIONS"]
    allow_headers=["*"],
)
class PromptInput(BaseModel):
    prompt: str

class PromptRequest(BaseModel):
    prompt: str = "We need a data analyst with good numerical reasoning and Excel knowledge, mid-level experience with test durations less than 60."
    top_k: int = 10

KEY_MAPPING = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

@app.get("/")
def read_root():
    return {"message": "SHL Recommender API is up 🚀"}


@app.get("/health")
def health_status():
    return {
        "status": "healthy",
        "message": "API is healthy and running ✅"
    }
@app.post("/recommend")
async def recommend(payload: PromptRequest):
    recommendations = recommend_tests(payload.prompt, payload.top_k)
    results = []
    mapped_keys = []
    for score, test in recommendations:
        mapped_keys = [KEY_MAPPING.get(k, k) for k in test.get("keys", [])]

    
    for score, test in recommendations:
        results.append({
            "name": test.get("name", "Unnamed"),
            "link": test.get("link", "#"),
            "duration": test.get("assessment_length", "N/A"),
            "remote_support": "Yes" if test.get("remote_available") == "Yes" else "No",
            "adaptive_support": "Yes" if test.get("adaptive_irt") == "Yes" else "No",
            "job_levels": test.get("job_levels", []),
            "skills": mapped_keys,
            "description": test.get("description", "No description available.")
        })
    return {"recommendations": results}


@app.get("/recommend")
async def recommend_docs():
    return {
       
        "IMP_MESSAGE ": "THIS IS AN EXAMPLE, TO TRY OUT THE API GO TO https://shl-recommendation-engine-hnys.onrender.com/docs#/default/recommend_recommend_post ",
        "message": "Send a POST request with a hiring prompt and top_k value.",
        "example_input": {
            "prompt": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
            "top_k": 1
        },
        "example_output": {
              "recommendations": [
    {
      "test-name": "MS Excel (New)",
      "link": "https://www.shl.com/solutions/products/product-catalog/view/ms-excel-new/",
      "duration (mins) ": 6,
      "remote available": "YES",
      "adaptive support": "NO",
      "job_levels": [
        "Job levelsEntry-Level",
        "Graduate",
        "Manager",
        "Mid-Professional",
        "Professional Individual Contributor",
        "Supervisor",
        ""
      ],
      "skills": [
        "Knowledge & Skills"
      ],
      "description": "DescriptionMulti-choice test that measures the ability to use MS Excel to maintain, organize, analyze and present numeric data."
    }
  ]
        }
    }