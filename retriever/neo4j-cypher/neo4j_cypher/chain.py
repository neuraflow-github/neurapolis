from typing import List, Union

from langchain.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain_community.graphs import Neo4jGraph
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# database = os.getenv("NEO4J_DATABASE")

# Connection to Neo4jen
graph = Neo4jGraph()

# Cypher validation tool for relationship directions
corrector_schema = [
    Schema(el["start"], el["type"], el["end"])
    for el in graph.structured_schema.get("relationships")
]
cypher_validation = CypherQueryCorrector(corrector_schema)

import os

from langchain_aws import ChatBedrock

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# LLMs
cypher_llm = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_kwargs={"temperature": 0.0},
)
qa_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

# Generate Cypher statement based on natural language input
cypher_template = """Based on the Neo4j graph schema below, write a Cypher query that would answer the user's question:
{schema}

When searching for specific information in the text chunks, never use the CONTAINS clause, instead use the vector search to then get the file content

Example semantic search query with dynamic embeddings:
```cypher
{examples}
```
Question: {question}

REMEMBER NOT TO INCLUDE A PREAMBLE, ONLY PURE CYPHER. in your queries. In your queries, DO NOT USE ANY RELATIONSHIPS OTHER THAN is_child_chunk.

Cypher query:"""

cypher_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question, convert it to a Cypher query. No pre-amble.",
        ),
        ("human", cypher_template),
    ]
)

from langchain_core.runnables import chain


@chain
def log(x, config, value=None):
    if value:
        print("\033[38;5;208m", value + str(x) + "\033[0m")
    else:
        print("\033[38;5;208m", "Logging: " + str(x) + "\033[0m")

    return x


from .selector import get_fewshot_examples

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


cypher_response = (
    RunnablePassthrough.assign(
        schema=lambda _: graph.get_schema,
        examples=lambda _: get_fewshot_examples(OPENAI_API_KEY, "question"),
    )
    | cypher_prompt
    | cypher_llm.bind(stop=["\nCypherResult:"])
    | StrOutputParser()
    | log
)

response_system = """You are an assistant that helps to form nice and human 
understandable answers based on the provided information from tools.
Do not add any other information that wasn't present in the tools, and use 
very concise style in interpreting results!
"""

response_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=response_system),
        HumanMessagePromptTemplate.from_template("{question}"),
        MessagesPlaceholder(variable_name="function_response"),
    ]
)


def get_function_response(
    query: str, question: str
) -> List[Union[AIMessage, ToolMessage]]:

    context = graph.query(cypher_validation(query))
    # TOOL_ID = "call_H7fABDuzEau48T10Qn0Lsh0D"
    # messages = [
    #     AIMessage(
    #         content="",
    #         additional_kwargs={
    #             "tool_calls": [
    #                 {
    #                     "id": TOOL_ID,
    #                     "function": {
    #                         "arguments": '{"question":"' + question + '"}',
    #                         "name": "GetInformation",
    #                     },
    #                     "type": "function",
    #                 }
    #             ]
    #         },
    #     ),
    #     ToolMessage(content=str(context)[:1000], tool_call_id=TOOL_ID),
    # ]
    return str(context)[:1000]
    return messages


from operator import itemgetter

chain = (
    RunnablePassthrough.assign(query=cypher_response)
    | RunnablePassthrough.assign(
        function_response=lambda x: get_function_response(x["query"], x["question"])
    )
    | itemgetter("function_response")
    # | response_prompt
    # | qa_llm
    # | StrOutputParser()
)

# Add typing for input


class Question(BaseModel):
    question: str


chain = chain.with_types(input_type=Question)
