cypher_template = """
Create a Cypher query to pre-filter and extract structure from the input question in a Neo4j graph database. The query should:

1. Identify relevant node types and relationships based on the question
2. Apply structural filters using non-text properties (dates, numbers, booleans)
3. Extract key structural elements to narrow down the solution space

Key points:
- Focus on identifying relevant patterns and structures
- Use only relationships and non-text properties for filtering
- Do not perform text-based searches or comparisons
- Return a simplified view of the relevant subgraph

Key node types: File, FileSection, FileChunk, Meeting, AgendaItem, Paper, Person, Organization

Query structure:
MATCH (start:RelevantStartNode)
WHERE <structural_conditions>
WITH start
MATCH (start)-[r:RELEVANT_RELATIONSHIP*..3]-(related)
WHERE <additional_structural_filters>
RETURN DISTINCT
    labels(start) AS start_labels,
    start.id AS start_id,
    [type(rel) IN r | type(rel)] AS relationship_types,
    labels(related) AS related_labels,
    related.id AS related_id,
    CASE WHEN 'File' IN labels(related) THEN related.access_url END AS file_url

Schema: {schema}
Question: {question}
Cypher query:
"""
