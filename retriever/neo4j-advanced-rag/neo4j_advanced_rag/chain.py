from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import ConfigurableField, RunnableParallel
from langchain_openai import ChatOpenAI
from neo4j import GraphDatabase

from neo4j_advanced_rag.retrievers import (
    # hypothetic_question_vectorstore,
    parent_vectorstore,
    # summary_vectorstore,
    typical_rag,
)

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

# Initialize Neo4j driver with error handling
try:
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    )
    # Verify the connection
    with driver.session() as session:
        session.run("RETURN 1")
except Exception as e:
    print(f"Failed to connect to Neo4j: {str(e)}")
    driver = None


def format_docs(docs):
    return "\n\n".join(
        f"{doc.page_content}\nSource: {doc.metadata.get('source', 'Unknown')}"
        for doc in docs
    )


template = """Answer the question based only on the following context, and always provide the source of the referenced information:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(model="gpt-4o-mini")

retriever = typical_rag.as_retriever().configurable_alternatives(
    ConfigurableField(id="strategy"),
    default_key="typical_rag",
    parent_strategy=parent_vectorstore.as_retriever(),
    # hypothetical_questions=hypothetic_question_vectorstore.as_retriever(),
    # summary_strategy=summary_vectorstore.as_retriever(),
)

# chain = (
#     RunnableParallel(
#         {
#             "context": itemgetter("question") | retriever | format_docs,
#             "question": itemgetter("question"),
#         }
#     )
#     | prompt
#     | model
#     | StrOutputParser()
# )

chain = itemgetter("question") | retriever | format_docs


# Add typing for input
class Question(BaseModel):
    question: str


chain = chain.with_types(input_type=Question)
