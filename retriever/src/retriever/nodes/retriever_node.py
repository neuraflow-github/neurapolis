from langchain_core.runnables.config import RunnableConfig
from neo4j.exceptions import DatabaseError, ServiceUnavailable

from retriever.config import config as retriever_config
from retriever.services.db_session_builder import db_session_builder
from retriever.state.file_chunk_state import FileChunkState
from retriever.state.hit_state import HitState
from retriever.state.search_state import SearchState

"""
WITH genai, vector. encode("Bau", "AzureOpenAI", {
token: "58469bb30d274655abb1830fc62faadd", resource: "neuraflow-eastus", deployment: "text-embedding-ada-002"|
5 }) AS queryVector
6 MATCH (p:Paper)-[:PAPER_HAS_AUXILIARY_FILE]->(f:File)-[:FILE_HAS_FILE_SECTION]->(fs:FileSection)-[:FILE_SECTION_HAS_FILE_CHUNK]->(fc:FileChunk)
WHERE p. reference = 'BaUStA-24/004' and fc. embedding IS NOT NULL
8 RETURN fc.id, fc.text, vector.similarity.cosine(fc.embedding, queryVector) AS similarity, p.reference
9 ORDER BY similarity DESC
10 LIMIT 10
"""


def retriever_node(search_state: SearchState, config: RunnableConfig):
    print("YXCVYXCV")
    print(config["configurable"])
    try:
        with db_session_builder.build() as db_session:
            db_query = f"""
            WITH genai.vector.encode("{search_state.query}", "AzureOpenAI", {{
                token: "{retriever_config.azure_openai_api_key}",
                resource: "{retriever_config.azure_openai_resource}",
                deployment: "text-embedding-ada-002"
            }}) AS queryVector
            MATCH (file_chunk_node:FileChunk)
            RETURN file_chunk_node.id, file_chunk_node.text, vector.similarity.cosine(file_chunk_node.embedding, queryVector) AS similarity
            ORDER BY similarity DESC
            LIMIT {10}
            """
            print(db_query)
            file_chunks_db_result = db_session.run(db_query)
        file_chunks: list[FileChunkState] = []
        for file_chunk_db_dict in file_chunks_db_result:
            file_chunk = FileChunkState.from_db_dict(file_chunk_db_dict)
            file_chunks.append(file_chunk)
        hits: list[HitState] = []
        for file_chunk in file_chunks:
            hit = HitState(
                file_chunk_id=file_chunk.id,
                file_chunk=file_chunk,
                file_section_id=file_chunk.file_section_id,
            )
            hits.append(hit)
        search_state.hits = hits
    except (ServiceUnavailable, DatabaseError) as e:
        print(f"Database connection error: {str(e)}")
        search_state.error = f"Database connection failed: {str(e)}"
        return {"searches": [search_state]}
    except Exception as e:
        print(f"Unexpected error in retriever_node: {str(e)}")
        search_state.error = f"An unexpected error occurred: {str(e)}"
        return {"searches": [search_state]}
    return {"searches": [search_state]}
