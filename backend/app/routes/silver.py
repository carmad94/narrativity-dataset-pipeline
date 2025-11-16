from fastapi import APIRouter
from app.database import transform_to_silver

router = APIRouter()

@router.post("/silver")
async def silver_transform():
    # Normalize data into structured format
    transform_to_silver()
    return {"message": "Silver layer transformation complete"}