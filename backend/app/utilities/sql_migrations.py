import os
import psycopg2
import logging
from dotenv import load_dotenv
from supabase import create_client
from app.constants import metadata_table_name, bronze_table_name, silver_table_name, golden_table_name
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SECRET_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration(sql_file_path):
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        raise RuntimeError("SUPABASE_DB_URL environment variable not set.")
    with open(sql_file_path, "r") as f:
        sql_template = f.read()
    sql = sql_template.format(
        metadata_table_name=metadata_table_name,
        bronze_table_name=bronze_table_name,
        silver_table_name=silver_table_name,
        golden_table_name=golden_table_name
    )
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    print(f"Migration applied: {sql_file_path}")