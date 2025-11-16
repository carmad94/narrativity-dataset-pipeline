from fastapi import APIRouter
from app.database import enrich_with_ai

router = APIRouter()

@router.post("/gold")
async def gold_enrichment():
    # Enrich data with OpenAI API
    enrich_with_ai()
    return {"message": "Gold layer enrichment complete"}