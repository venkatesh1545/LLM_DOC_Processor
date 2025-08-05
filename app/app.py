# from fastapi import APIRouter, HTTPException
# from app.models import ClaimRequest, DecisionResponse
# from app.query_handler import process_query
# from app.vector_store import VectorDB
# from app.decision_engine import make_decision

# router = APIRouter()

# # Assume vector_db is initialized globally for demo
# @router.post("/process-claim", response_model=DecisionResponse)
# async def process_claim_query(request: ClaimRequest):
#     entities = process_query(request.query)
#     # Semantic search and clause retrieval
#     clauses = [c[0] for c in vector_db.query(request.query, top_k=5)]
#     result = make_decision(entities, clauses)
#     return DecisionResponse(**result)
