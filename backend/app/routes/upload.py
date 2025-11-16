from fastapi import APIRouter, UploadFile, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import insert_file_metadata

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/upload")
@limiter.limit("2/minute")
async def upload_file(request: Request, file: UploadFile):
    filename = file.filename.lower()
    if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
        raise HTTPException(
            status_code=400,
            detail="Only .csv or .xlsx files are allowed."
        )
    try:
        contents = await file.read()

        return insert_file_metadata(contents, filename, file.content_type)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")