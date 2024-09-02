from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Typical RAG retriever

typical_rag = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(), index_name="file_chunks"
)

# # Parent retriever

parent_query = """
MATCH (node)<-[:FILE_SECTION_HAS_FILE_CHUNK]-(parent)
WITH parent, max(score) AS score // deduplicate parents
RETURN parent.text AS text, score, {} AS metadata LIMIT 5
"""

parent_vectorstore = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(),
    index_name="file_chunks",
    retrieval_query=parent_query,
)

# # Hypothetic questions retriever

hypothetic_question_query = """
MATCH (node)<-[:HAS_QUESTION]-(parent)
WITH parent, max(score) AS score // deduplicate parents
RETURN parent.text AS text, score, {} AS metadata
"""

# hypothetic_question_vectorstore = Neo4jVector.from_existing_index(
#     OpenAIEmbeddings(),
#     index_name="hypothetical_questions",
#     retrieval_query=hypothetic_question_query,
# )
# # Summary retriever

summary_query = """
MATCH (node)<-[:HAS_SUMMARY]-(parent)
WITH parent, max(score) AS score // deduplicate parents
RETURN parent.text AS text, score, {} AS metadata
"""

# summary_vectorstore = Neo4jVector.from_existing_index(
#     OpenAIEmbeddings(),
#     index_name="summary",
#     retrieval_query=summary_query,
# )
