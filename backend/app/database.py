import pandas as pd
from io import BytesIO
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
from app.constants import *
import os
import hashlib
import logging
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SECRET_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_file_metadata(contents, filename, content_type):
    content = BytesIO(contents)
    if filename.endswith(".csv"):
        df = pd.read_csv(content)
    else:
        df = pd.read_excel(content, engine="openpyxl")

    # Convert DataFrame to JSON
    # df.fillna("", inplace=True)
    # data_json = df.to_dict(orient="records")
    rows_to_insert = [{
        "filename": filename,
        "num_rows": df.shape[0],
        "content_type": content_type,
        "uploaded_date": datetime.now().isoformat()
    }]
    insert_records(metadata_table_name, rows_to_insert)
    insert_raw_data(df)
    return {"filename": filename, "rows": df.shape[0], "content_type": content_type}

def insert_raw_data(df):
    df['pd'] = pd.to_datetime(df['pd'], errors='coerce')
    df['is'] = df['is'].apply(lambda x: int(x.timestamp()) if isinstance(x, datetime) else x)
    for col in df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    for col in columns_cast_to_int:
        df[col] = df[col].fillna(0).astype(int)
    df = df.where(pd.notnull(df), None)
    df = df.fillna("")
    data_json = df.to_dict(orient="records")

    # preparing json to insert data
    insert_data = []
    uploaded_date = datetime.now().isoformat()
    for item in data_json:
        item_to_insert = {}
        item_to_insert["raw_data"] = item
        item_to_insert["hash"] = compute_hash(item)
        item_to_insert["uploaded_date"] = uploaded_date
        insert_data.append(item_to_insert)
    logger.info(f"Inserting to {bronze_table_name}")
    insert_records(bronze_table_name, insert_data, ["hash"])
    transform_to_silver(insert_data, df)

def transform_to_silver(insert_data: list,df: pd.DataFrame):
    df_bronze = pd.DataFrame(insert_data)
    df_final = pd.concat([df, df_bronze["hash"]], axis=1)
    df_final.to_csv("test.csv", index=False)
    df_final.loc[df_final["title"] == "", "title"] = df_final["ti"]
    df_final.loc[df_final["au"] == "", "au"] = df_final["firstauthor"]
    df_final.drop(
        columns=columns_to_delete,
        inplace=True
    )
    cols_to_drop = [col for col in df.columns if col.startswith('X_')]
    df_final.drop(columns=cols_to_drop, inplace=True)
    df_final.rename(columns=columns_to_rename, inplace=True)
    df_final.columns = [col.lower() for col in df_final.columns]
    df_final_json = df_final.to_dict(orient="records")
    logger.info(f"Inserting to {silver_table_name}")
    insert_records(silver_table_name, df_final_json)

def enrich_with_ai(id: int):
    logger.info(f"Enriching with AI: {id}")
    silver_record = get_record_by_id(table_name=silver_table_name, key_value=id)
    silver_record = json.loads(silver_record.json())
    sample = silver_record["data"][0]
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = get_custom_prompt(sample)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300  # Adjust token limit as needed
    )
    enriched_data = response.choices[0].message.content
    enriched_records = [{
        "silver_id": id,
        "description": enriched_data
    }]
    insert_records(golden_table_name, enriched_records, ["silver_id"])
    return enriched_data

def get_enriched_story(id:int=1):
    logger.info(f"Getting enriched story: {id} from {golden_table_name}")
    sample = get_record_by_id(golden_table_name, "silver_id", id)
    sample = json.loads(sample.json())
    if sample["data"]:
        return sample["data"][0]["description"]
    else:
        return enrich_with_ai(id)


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