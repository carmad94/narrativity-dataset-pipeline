from fastapi import FastAPI
from app.routes import upload, bronze, story
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .constants import origin, create_metadata_table_sql, create_bronze_table_sql, create_silver_table_sql, create_gold_table_sql
from .database import create_table

app = FastAPI()
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # or specify: ["GET", "POST"]
    allow_headers=["*"],  # or specify: ["Authorization", "Content-Type"]
)

# Include routers
app.include_router(upload.router)
app.include_router(bronze.router)
app.include_router(story.router)

create_table(create_metadata_table_sql)
create_table(create_bronze_table_sql)
create_table(create_silver_table_sql)
create_table(create_gold_table_sql)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Data Platform!"}