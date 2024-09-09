import os
import sys
from dotenv import load_dotenv
from tqdm import tqdm
from neo4j import GraphDatabase
from langchain_openai import AzureOpenAIEmbeddings
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set PYTHONPATH at the start of the script
sys.path.insert(0, "/Users/pascal/ris/")

# Load environment variables
load_dotenv(override=True)

# Initialize embeddings
embeddings = AzureOpenAIEmbeddings()

# Initialize Neo4j Aura connection
uri = os.getenv("DB_URI")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

# Ensure the URI uses the 'neo4j+s' scheme for Neo4j Aura
if uri and not uri.startswith("neo4j+s://"):
    uri = f"neo4j+s://{uri.split('://')[-1]}"

# Create the driver with Neo4j Aura settings
driver = GraphDatabase.driver(
    uri,
    auth=(username, password),
    max_connection_lifetime=30 * 60,  # 30 minutes
    max_connection_pool_size=50,
    connection_acquisition_timeout=2 * 60,  # 2 minutes
)

# Verify the connection
try:
    with driver.session() as session:
        session.run("RETURN 1")
    logging.info("Successfully connected to Neo4j database")
except Exception as e:
    logging.error(f"Error connecting to Neo4j: {str(e)}")
    driver.close()
    raise


def get_file_chunks(limit=25, offset=0):
    """
    Retrieve file chunks from the database that don't have embeddings.

    Args:
        limit (int): Maximum number of chunks to retrieve.
        offset (int): Number of chunks to skip.

    Returns:
        list: A list of tuples containing chunk IDs and texts.
    """
    with driver.session() as session:
        result = session.run(
            "MATCH (c:FileChunk) WHERE c.embedding IS NULL "
            "RETURN c.id AS id, c.text AS text "
            "SKIP $offset LIMIT $limit",
            offset=offset,
            limit=limit,
        )
        return [(record["id"], record["text"]) for record in result]


def update_file_chunk_with_embedding(tx, chunk_id, embedding):
    """
    Update a file chunk in the database with its embedding.

    Args:
        tx: The database transaction.
        chunk_id (str): The ID of the chunk to update.
        embedding (list): The embedding vector to set for the chunk.
    """
    tx.run(
        "MATCH (c:FileChunk {id: $id}) SET c.embedding = $embedding",
        id=chunk_id,
        embedding=embedding,
    )


def process_file_chunks():
    """
    Process file chunks by generating embeddings and updating the database.

    This function retrieves chunks without embeddings, generates embeddings for them,
    and updates the database with the new embeddings. It includes error handling and
    retries for robustness.
    """
    offset = 0
    max_retries = 3
    while True:
        file_chunks = get_file_chunks(limit=25, offset=offset)
        if not file_chunks:
            break

        with driver.session() as session:
            for chunk_id, chunk_text in tqdm(
                file_chunks,
                desc=f"Processing chunks {offset+1}-{offset+len(file_chunks)}",
                unit="chunk",
            ):
                for attempt in range(max_retries):
                    try:
                        embedding = embeddings.embed_query(chunk_text)
                        session.execute_write(
                            update_file_chunk_with_embedding, chunk_id, embedding
                        )
                        break
                    except Exception as e:
                        if attempt < max_retries - 1:
                            logging.warning(
                                f"Error processing chunk {chunk_id}. Retrying... (Attempt {attempt + 1}/{max_retries})"
                            )
                            time.sleep(2**attempt)  # Exponential backoff
                        else:
                            logging.error(
                                f"Failed to process chunk {chunk_id} after {max_retries} attempts. Error: {str(e)}"
                            )

        offset += 25


def create_vector_index():
    """
    Create a vector index in the database for efficient similarity searches.

    This function checks if the index already exists and creates it if it doesn't.
    """
    with driver.session() as session:
        try:
            # Check if the index already exists
            result = session.run(
                "SHOW INDEXES WHERE type = 'VECTOR' AND name = 'file_chunks'"
            )
            if not list(result):
                session.run(
                    "CALL db.index.vector.createNodeIndex('file_chunks', 'FileChunk', 'embedding', 1536, 'cosine')"
                )
                logging.info("Created file_chunks index successfully")
            else:
                logging.info("file_chunks index already exists")
        except Exception as e:
            logging.error(f"Error creating or checking file_chunks index: {str(e)}")


def verify_all_chunks_processed():
    """
    Verify that all file chunks have been processed and have embeddings.

    This function checks for any remaining chunks without embeddings and logs the result.
    """
    with driver.session() as session:
        result = session.run(
            "MATCH (c:FileChunk) WHERE c.embedding IS NULL RETURN COUNT(c) as count"
        )
        unprocessed_count = result.single()["count"]
        if unprocessed_count > 0:
            logging.warning(f"There are still {unprocessed_count} unprocessed chunks.")
        else:
            logging.info("All chunks have been processed successfully.")


# Main execution
if __name__ == "__main__":
    create_vector_index()
    process_file_chunks()
    verify_all_chunks_processed()

    # Close the driver connection
    driver.close()
