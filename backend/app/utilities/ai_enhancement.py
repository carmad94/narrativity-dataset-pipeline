import logging
import os
import json
from dotenv import load_dotenv
import openai
from app.constants import *
from app.database import *

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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