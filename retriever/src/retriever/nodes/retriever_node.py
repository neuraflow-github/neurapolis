from langchain_core.runnables.config import RunnableConfig
from neo4j.exceptions import DatabaseError, ServiceUnavailable

from retriever.config import config as retriever_config
from retriever.services.db_session_builder import db_session_builder
from retriever.state.file_chunk_state import FileChunkState
from retriever.state.hit_state import HitState
from retriever.state.hit_step import HitStep
from retriever.state.search_state import SearchState
from retriever.state.search_step import SearchStep

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
    # print("YXCVYXCV")
    # print(config["configurable"])
    with db_session_builder.build() as db_session:
        # TODO use variables here
        db_query = """
        WITH genai.vector.encode($user_query, "AzureOpenAI", {
            token: "8ec005db5f0e4b32bbac0616b95d9391",
            resource: "neuraflow-swedencentral",
            deployment: "text-embedding-ada-002"
        }) AS query_vector
        MATCH (file_chunk_node:FileChunk)<-[:FILE_SECTION_HAS_FILE_CHUNK]-(file_section_node:FileSection)
        RETURN file_chunk_node, file_section_node.id AS file_section_id, vector.similarity.cosine(file_chunk_node.embedding, query_vector) AS similarity
        ORDER BY similarity DESC
        LIMIT $limit
        """
        file_chunk_db_results = db_session.run(
            db_query,
            user_query=search_state.query,
            azure_open_ai_api_key=retriever_config.azure_openai_api_key,
            azure_open_ai_resource=retriever_config.azure_openai_resource,
            limit=10,
        )
        file_chunks: list[FileChunkState] = []
        for x_file_chunk_db_result in file_chunk_db_results:
            file_chunk = FileChunkState.from_db_dict(
                x_file_chunk_db_result["file_chunk_node"],
                x_file_chunk_db_result["file_section_id"],
            )
            file_chunks.append(file_chunk)
    hits: list[HitState] = []
    for file_chunk in file_chunks:
        hit = HitState(
            step=HitStep.RETRIEVED,
            file_chunk=file_chunk,
        )
        hits.append(hit)
    search_state.step = SearchStep.RETRIEVED
    search_state.hits = hits
    return {"searches": [search_state]}
