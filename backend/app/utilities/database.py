from supabase import create_client
from dotenv import load_dotenv
from app.constants import *
import os
import hashlib
import logging

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SECRET_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compute_hash(row):
    raw_json = str(row)  # Convert the row (JSON) to a string
    return hashlib.sha256(raw_json.encode()).hexdigest()

def create_table(create_table_sql: str)->bool:
    try:
        logger.info(f"Creating table using {create_table_sql}")
        supabase.postgrest.rpc("exec_sql", {"sql": create_table_sql}).execute()
        return True
    except Exception:
        # If RPC is not set up, use the SQL Editor in Supabase dashboard or psycopg2
        from psycopg2 import connect
        import urllib.parse as up

        # Parse connection string from Supabase
        conn_str = os.getenv('SUPABASE_DB_URL')
        if not conn_str:
            raise ValueError("Set SUPABASE_DB_URL for direct Postgres connection.")

        conn = connect(conn_str)
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        return True
    return False

def insert_records(table_name: str, data_to_insert: list, on_conflict:list=["id"]):
    # logger.info(data_to_insert)
    data_len = len(data_to_insert)
    batch_size = 500 if 500 < data_len else data_len
    # Upsert data in batches
    for i in range(0, data_len, batch_size):
        batch = data_to_insert[i:i + batch_size]
        try:
            supabase.table(table_name).upsert(batch, on_conflict=on_conflict).execute()
            print("Rows inserted (duplicates skipped).")
        except Exception as e:
            print("Error inserting rows:", e)


def get_records(table_name: str, start: int=0, end: int=10):
    try:
        response = supabase.table(table_name).select("*").order('id').range(start, end).execute()
        logger.info("Get all records from table.")
        return response
    except Exception as e:
        print("Error inserting rows:", e)

def get_record_by_id(table_name: str, key_name:str="id", key_value:int=1):
    try:
        response = supabase.table(table_name).select("*").eq(key_name, key_value).execute()
        return response
    except Exception as e:
        print("Error inserting rows:", e)

def get_table_count(table_name: str, key_name:str="id"):
    try:
        response = supabase.table(table_name).select(key_name, count="exact").execute()
        return response
    except Exception as e:
        print("Error inserting rows:", e)