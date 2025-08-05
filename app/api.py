from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, HttpUrl
from typing import List
import logging
from app.doc_ingest import ingest
from app.query_handler import run_query

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1")

# === AUTH =================================================================
BEARER_TOKEN = (
    "f54ada5ff8aad823c950caee24b08bafd5d45da70027d16daef3f21f49af01e9"
)

def check_auth(authorization: str = Header(...)):
    if not authorization.replace("Bearer ", "") == BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# === SCHEMAS ==============================================================

class RunRequest(BaseModel):
    documents: str
    questions: List[str]

class RunResponse(BaseModel):
    answers: List[str]

# === ENDPOINT ==============================================================

@router.post("/hackrx/run", response_model=RunResponse, dependencies=[Depends(check_auth)])
def hackrx_run(payload: RunRequest):
    try:
        logger.info(f"Processing request with document: {payload.documents}")
        logger.info(f"Questions: {payload.questions}")
        
        # Convert single URL to list for ingest function
        ingest([payload.documents])
        logger.info("Document ingestion completed")
        
        answers = []
        for q in payload.questions:
            logger.info(f"Processing question: {q}")
            result = run_query(q)
            logger.info(f"Query result: {result}")
            answers.append(result["answer"])
        
        logger.info(f"Returning answers: {answers}")
        return {"answers": answers}
        
    except Exception as e:
        logger.error(f"Error in hackrx_run: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

