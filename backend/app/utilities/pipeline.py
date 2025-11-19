import pandas as pd
from io import BytesIO
from datetime import datetime
from app.constants import *
from app.database import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_file_metadata(contents, filename, content_type):
    content = BytesIO(contents)
    if filename.endswith(".csv"):
        df = pd.read_csv(content)
    else:
        df = pd.read_excel(content, engine="openpyxl")

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