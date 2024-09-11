from langchain_core.runnables.config import RunnableConfig

from retriever.config import config as retriever_config
from retriever.services.db_session_builder import db_session_builder
from retriever.state.file_chunk_state import FileChunkState
from retriever.state.hit_state import HitState
from retriever.state.hit_step import HitStep
from retriever.state.search_state import SearchState
from retriever.state.search_step import SearchStep
from retriever.state.search_type import SearchType


def retriever_node(search_state: SearchState, config: RunnableConfig):
    # print("YXCVYXCV")
    # print(config["configurable"])
    file_chunks: list[FileChunkState] = []
    if search_state.type == SearchType.VECTOR:
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
            db_results = db_session.run(
                db_query,
                user_query=search_state.query,
                azure_open_ai_api_key=retriever_config.azure_openai_api_key,
                azure_open_ai_resource=retriever_config.azure_openai_resource,
                limit=10,
            )
            for x_db_result in db_results:
                file_chunk = FileChunkState.from_db_dict(
                    x_db_result["file_chunk_node"],
                    x_db_result["file_section_id"],
                )
                file_chunks.append(file_chunk)
    elif search_state.type == SearchType.KEYWORD:
        pass
        # with db_session_builder.build() as db_session:
        #     db_query = """
        #     CALL db.index.fulltext.queryNodes("file_chunk_texts", $user_query) YIELD file_chunk_node, score
        #     MATCH (file_chunk_node)<-[:FILE_SECTION_HAS_FILE_CHUNK]-(file_section_node:FileSection)
        #     RETURN file_chunk_node.text, file_section_node.id AS file_section_id, score
        #     """
        #     query_parts = search_state.query.split()
        #     fuzzy_words = []
        #     for x_query_part in query_parts:
        #         fuzzy_word = f"{x_query_part}~"
        #         fuzzy_words.append(fuzzy_word)
        #     fuzzy_lucene_query = " AND ".join(fuzzy_words)
        #     db_results = db_session.run(db_query, user_query=fuzzy_lucene_query)
        #     file_chunks: list[FileChunkState] = []
        #     for x_db_result in db_results:
        #         file_chunk = FileChunkState.from_db_dict(
        #             x_db_result["file_chunk_node"],
        #             x_db_result["file_section_id"],
        #         )
        #         file_chunks.append(file_chunk)
    else:
        raise ValueError(f"Invalid search type: {search_state.type}")
    for file_chunk in file_chunks:
        hit = HitState(
            step=HitStep.RETRIEVED,
            file_chunk=file_chunk,
        )
        search_state.hits.append(hit)
    search_state.step = SearchStep.RETRIEVED
    return {"searches": [search_state]}
