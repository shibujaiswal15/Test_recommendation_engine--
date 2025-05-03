from pydantic import BaseModel

class PromptInput(BaseModel):
    prompt: str

class RecommendedAssessment(BaseModel):
    id: str
    title: str
    description: str
    key: str