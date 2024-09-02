from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain.embeddings import OpenAIEmbeddings

example_prompt = PromptTemplate(
    input_variables=["query", "cypher"],
    template="Query: {query}\n\nCypher: {cypher}",
)

fewshot_examples = [
    {
        "query": "Find the file most relevant to climate change policies.",
        "cypher": """
        CALL {{
          WITH "climate change policies" AS searchPrompt
          WITH genai.vector.encode(searchPrompt, "AzureOpenAI", {{
            token: "58469bb30d274655abb1830fc62faadd",
            resource: "neuraflow-eastus",
            deployment: "text-embedding-ada-002"
          }}) AS queryVector
          CALL db.index.vector.queryNodes('file_chunks', 5, queryVector) YIELD node, score
          MATCH (f:File)-[:HAS_CHILD_CHUNK]->(node)
          RETURN f.name AS fileName, f.id AS fileId, node.text AS chunkText, score AS relevanceScore, f, node
          ORDER BY score DESC
          LIMIT 1
        }}
        RETURN f
        """,
    },
    {
        "query": "Which meetings discussed topics related to budget allocation?",
        "cypher": """
        CALL {{
          WITH "budget allocation" AS searchPrompt
          WITH genai.vector.encode(searchPrompt, "AzureOpenAI", {{
            token: "58469bb30d274655abb1830fc62faadd",
            resource: "neuraflow-eastus",
            deployment: "text-embedding-ada-002"
          }}) AS queryVector
          CALL db.index.vector.queryNodes('file_chunks', 5, queryVector) YIELD node, score
          MATCH (f:File)-[:HAS_CHILD_CHUNK]->(node)
          RETURN f.name AS fileName, f.id AS fileId, node.text AS chunkText, score AS relevanceScore, f, node
          ORDER BY score DESC
          LIMIT 1
        }}
        MATCH (m:Meeting)-[:HAS_AUXILIARY_FILE]->(f)
        RETURN DISTINCT m.name AS meetingName, m.start AS meetingDate, f.name AS fileName, node.text AS chunkText, score AS relevanceScore
        ORDER BY m.start DESC
        """,
    },
    {
        "query": "List all files containing information about urban development projects.",
        "cypher": """
        CALL {{
          WITH "urban development projects" AS searchPrompt
          WITH genai.vector.encode(searchPrompt, "AzureOpenAI", {{
            token: "58469bb30d274655abb1830fc62faadd",
            resource: "neuraflow-eastus",
            deployment: "text-embedding-ada-002"
          }}) AS queryVector
          CALL db.index.vector.queryNodes('file_chunks', 5, queryVector) YIELD node, score
          MATCH (f:File)-[:HAS_CHILD_CHUNK]->(node)
          RETURN f.name AS fileName, f.id AS fileId, node.text AS chunkText, score AS relevanceScore, f, node
          ORDER BY score DESC
        }}
        RETURN f.name AS fileName, f.id AS fileId, node.text AS chunkText, score AS relevanceScore
        """,
    },
    {
        "query": "Find agenda items related to environmental sustainability.",
        "cypher": """
        CALL {{
          WITH "environmental sustainability" AS searchPrompt
          WITH genai.vector.encode(searchPrompt, "AzureOpenAI", {{
            token: "58469bb30d274655abb1830fc62faadd",
            resource: "neuraflow-eastus",
            deployment: "text-embedding-ada-002"
          }}) AS queryVector
          CALL db.index.vector.queryNodes('file_chunks', 5, queryVector) YIELD node, score
          MATCH (f:File)-[:HAS_CHILD_CHUNK]->(node)<-[:HAS_AUXILIARY_FILE]-(m:Meeting)-[:HAS_AGENDA_ITEM]->(a:AgendaItem)
          RETURN a.name AS agendaItemName, m.name AS meetingName, f.name AS fileName, score AS relevanceScore, f, node
          ORDER BY score DESC
          LIMIT 5
        }}
        RETURN agendaItemName, meetingName, fileName, relevanceScore
        """,
    },
    {
        "query": "Which legislative term is most related to healthcare reforms?",
        "cypher": """
        CALL {{
          WITH "healthcare reforms" AS searchPrompt
          WITH genai.vector.encode(searchPrompt, "AzureOpenAI", {{
            token: "58469bb30d274655abb1830fc62faadd",
            resource: "neuraflow-eastus",
            deployment: "text-embedding-ada-002"
          }}) AS queryVector
          CALL db.index.vector.queryNodes('file_chunks', 5, queryVector) YIELD node, score
          MATCH (f:File)-[:HAS_CHILD_CHUNK]->(node)
          RETURN f.name AS fileName, f.id AS fileId, node.text AS chunkText, score AS relevanceScore, f, node
          ORDER BY score DESC
          LIMIT 1
        }}
        MATCH (lt:LegislativeTerm)-[:HAS_AUXILIARY_FILE|:HAS_PAPER|:HAS_RESULTS_PROTOCOL_FILE]->(f)
        RETURN DISTINCT lt.name AS legislativeTermName, f.name AS fileName, node.text AS chunkText, score AS relevanceScore
        ORDER BY score DESC
        """,
    },
    {
        "query": "Get information about an organization, its members, and consultations.",
        "cypher": """
        MATCH (o:Organization {name: $organizationName})
        OPTIONAL MATCH (o)-[:HAS_MEMBERSHIP]->(m:Membership)-[:HAS_PERSON]->(p:Person)
        OPTIONAL MATCH (o)-[:HAS_CONSULTATION]->(c:Consultation)
        RETURN o.name AS organizationName, collect(p.name) AS members, collect(c.name) AS consultations
        """,
    },
    {
        "query": "List all meetings for a given legislative term.",
        "cypher": """
        MATCH (lt:LegislativeTerm {name: $legislativeTermName})-[:HAS_MEETING]->(m:Meeting)
        RETURN m.name AS meetingName, m.start AS meetingDate
        ORDER BY m.start DESC
        """,
    },
    {
        "query": "Find files related to a specific meeting.",
        "cypher": """
        MATCH (m:Meeting {name: $meetingName})-[:HAS_MAIN_FILE|:HAS_AUXILIARY_FILE|:HAS_RESULTS_PROTOCOL_FILE]->(f:File)
        RETURN f.name AS fileName, f.id AS fileId
        ORDER BY f.name
        """,
    },
    {
        "query": "Identify the person in charge of a specific body.",
        "cypher": """
        MATCH (b:Body {name: $bodyName})-[:HAS_UNDER_DIRECTION_OF]->(p:Person)
        RETURN p.name AS personInCharge, p.title AS personTitle
        """,
    },
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
    fewshot_examples,
    OpenAIEmbeddings(),
    Chroma,
    k=3,
)

similar_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Use vector embeddings and similarity search to query unstructured data in the knowledge graph. Focus on the File and ChildChunk nodes, and utilize the genai.vector.encode and db.index.vector.queryNodes functions as shown in the examples. For structured queries, use appropriate Cypher patterns to retrieve information from specific node types and relationships.",
    suffix="Query: {query}\n\nCypher:",
    input_variables=["query"],
)


def get_fewshot_examples(openai_api_key, question):
    return similar_prompt.format(openai_api_key=openai_api_key, query=question)
