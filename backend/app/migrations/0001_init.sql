CREATE TABLE IF NOT EXISTS public.{metadata_table_name} (
    id SERIAL PRIMARY KEY,
    uploaded_date TIMESTAMP NOT NULL,
    filename TEXT NOT NULL,
    content_type TEXT NOT NULL,
    num_rows INT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.{bronze_table_name} (
    hash TEXT PRIMARY KEY,
    uploaded_date TIMESTAMP NOT NULL,
    raw_data jsonb NOT NULL
);

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

CREATE TABLE IF NOT EXISTS public.{golden_table_name} (
    ID SERIAL PRIMARY KEY,
    description TEXT,
    silver_id INT UNIQUE REFERENCES {silver_table_name}(id) ON DELETE CASCADE
);