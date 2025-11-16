origin=["http://localhost:3000"]

metadata_table_name = "metadata"
bronze_table_name = "raw_data"
silver_table_name = "normalized_data"
golden_table_name = "ai_enhanced"

create_metadata_table_sql = f"""
CREATE TABLE IF NOT EXISTS public.{metadata_table_name} (
    id SERIAL PRIMARY KEY,
    uploaded_date TIMESTAMP NOT NULL,
    filename TEXT NOT NULL,
    content_type TEXT NOT NULL,
    num_rows INT NOT NULL
);
"""

create_bronze_table_sql = f"""
CREATE TABLE IF NOT EXISTS public.{bronze_table_name} (
    hash TEXT PRIMARY KEY,
    uploaded_date TIMESTAMP NOT NULL,
    raw_data jsonb NOT NULL
);
"""

create_silver_table_sql = f"""
CREATE TABLE IF NOT EXISTS public.{silver_table_name} (
    ID SERIAL PRIMARY KEY,
    appeal_to_reader TEXT,
    conjunctions INT,
    connectivity INT,
    narrative_perspective TEXT,
    sensory_language INT,
    setting TEXT,
    abstract TEXT,
    pubMedID INT,
    publication_year INT,
    source TEXT,
    times_cited INT,
    author_affiliation TEXT,
    author TEXT,
    di TEXT,
    date_published TEXT,
    total_citations INT,
    numberauthors INT,
    title TEXT,
    hash TEXT UNIQUE REFERENCES {bronze_table_name}(hash) ON DELETE CASCADE
);
"""

create_gold_table_sql = f"""
CREATE TABLE IF NOT EXISTS public.{golden_table_name} (
    ID SERIAL PRIMARY KEY,
    description TEXT,
    silver_id INT UNIQUE REFERENCES {silver_table_name}(id) ON DELETE CASCADE
);
"""

columns_to_rename = {
    "ab": "abstract",
    "pmid": "pubMedID",
    "py": "publication_year",
    "so": "source",
    "tc": "times_cited",
    "af": "author_affiliation",
    "au": "author",
    "pd": "date_published",
    "z9": "total_citations"
}

columns_to_delete = ["Unnamed: 0", "bp", "ep", "is", "ut", "vl", "cin_mas", "pid_mas", "pt", "sn", "ti", "appeal_to_reader_gold", "conjunctions_gold", "connectivity_gold", "narrative_perspective_gold", "setting_gold", "sensory_language_gold", "firstauthor"]

columns_cast_to_int = ["conjunctions", "connectivity", "sensory_language", "bp", "vl", "z9", "cin_mas", "numberauthors", "pid_mas", "tc", "py", "pmid"]

def get_custom_prompt(sample: dict)->str:
    prompt = f"""The following data contains information or metadata of a scientific paper:\n\n
    Title: {sample["title"]}\n
    Abstract: {sample["abstract"]}\n
    Source: {sample["source"]}\n
    Publication year: {sample["publication_year"]}\n
    Times Cited: {sample["times_cited"]}\n
    Total Citation: {sample["total_citations"]}\n
    \n
    The following data contains the narrativity score annotated by an annotator:\n
    \n
    Appeal to reader: {sample['appeal_to_reader']}\n
    Conjunctions: {sample['conjunctions']}\n
    Connectivity: {sample['connectivity']}\n
    Narrative Perspective: {sample['narrative_perspective']}\n
    Sensory Language: {sample['sensory_language']}\n
    Setting: {sample['setting']}\n
    \n
    Your task is to enrich this record by briefly explaining the scientific paper 
    and its corresponding narrativity score. 
    Explain briefly the paper in one sentence. 
    Then Explain and summarize in human terms and from the annotator's perspective
    what the data for narrativity score meant.
    Please answer it in less than or equal to 100 words and focus in explaining the narrativity score
    for the scientific paper"""
    return prompt