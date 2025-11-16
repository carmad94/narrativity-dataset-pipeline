from fastapi import APIRouter, Request, Query
from app.database import get_records, get_table_count
from app.constants import silver_table_name
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/bronze")
@limiter.limit("10/minute")
async def bronze_ingest(request: Request,
                        page: int = Query(1, ge=1, description="Page number (starting from 1)"),
                        page_size: int = Query(100, ge=1, le=100, description="Number of items per page")
                        ):
    start = (page - 1) * page_size
    end = start + page_size - 1
    records = get_records(silver_table_name, start, end).data
    total_records = get_table_count(silver_table_name).count
    return {
        "records": records,
        "total": total_records
    }