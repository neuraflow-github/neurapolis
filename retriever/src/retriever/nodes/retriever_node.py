from langchain_core.runnables.config import RunnableConfig
from neo4j.exceptions import DatabaseError, ServiceUnavailable

from retriever.config import config as retriever_config
from retriever.services.db_session_builder import db_session_builder
from retriever.state.file_chunk_state import FileChunkState
from retriever.state.hit_state import HitState
from retriever.state.hit_step import HitStep
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
    with db_session_builder.build() as db_session:
        db_query = f"""
        MATCH (file_chunk_node:FileChunk)
        RETURN file_chunk_node
        LIMIT 10
        """
        print(db_query)
        file_chunks_db_result = db_session.run(db_query)
        file_chunks: list[FileChunkState] = []
        for x_file_chunk_db_dict in file_chunks_db_result:
            file_chunk = FileChunkState.from_db_dict(
                x_file_chunk_db_dict["file_chunk_node"]
            )
            file_chunks.append(file_chunk)
        print("JHGFJHGF")
        print(file_chunks)
    hits: list[HitState] = []
    for file_chunk in file_chunks:
        hit = HitState(
            step=HitStep.RETRIEVED,
            file_chunk=file_chunk,
        )
        hits.append(hit)
    search_state.hits = hits
    return {"searches": [search_state]}
