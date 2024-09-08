# ETL

## Environment variables

- `API_URL`
- `DATASTORE_DIR_PATH`
- `DB_NAME`
- `DB_PASSWORD`
- `DB_URI`
- `DB_USERNAME`

## Setup

- Install packages: Run `poetry install`
- Clear Neo4j database: Run `CALL apoc.periodic.iterate(
  "MATCH (n) RETURN n",
  "DETACH DELETE n",
  {batchSize:1000}
)
YIELD batches, total
RETURN batches, total`

## Run

- Activate poetry shell: Run `poetry shell`
- Run `python main.py`

- Installed brew install tesseract and brew install poppler and brew install tesseract-deu
- brew install libmagic

## Commands

- Delete all file sections and file chunks: `MATCH (n:FileSection) DETACH DELETE n; MATCH (n:FileChunk) DETACH DELETE n;`

## Cost

- Per page reconstruction
  - Input tokens: 3700 = 
  - Output tokens: 650 = 
- Pages per file: 
- Sectionizer cost per file:
  - Input tokens: 
  - Output tokens: 
