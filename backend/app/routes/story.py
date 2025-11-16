from fastapi import APIRouter,  Request
from app.database import get_enriched_story
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/generate-story/{id}")
@limiter.limit("3/minute")
async def generate_story(request: Request, id: int):
    # Generate story using enriched data
    story = get_enriched_story(id)
    return {"summary": story}