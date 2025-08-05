from pydantic import BaseModel
from typing import List

class HackRxRequest(BaseModel):
    documents: str   # URL to PDF
    questions: List[str]

class HackRxResponse(BaseModel):
    answers: List[str]
