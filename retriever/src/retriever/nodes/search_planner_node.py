import uuid
from datetime import datetime
from operator import itemgetter
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from retriever.state.search_state import SearchState
from retriever.state.search_type import SearchType
from retriever.state.state import State


class SearchPlannerLlmDataModel(BaseModel):
    vector_search_querires: List[str] = Field(
        description="Die Suchanfragen, die der Retriever an die Vektordatenbank stellen soll"
    )
    keyword_search_queries: List[str] = Field(
        description="Die Suchanfragen, die der Retriever an die Keyword-Datenbank stellen soll"
    )


def search_planner_node(state: State):
    # TODO Beispiele
    prompt_template_string = """
    Generell:
    - Du bist der "Search-Planner"-Mitarbeiter bei der deutschen Stadt Freiburg.
    - Du und deine Kollegen seid für das Rats Informations System (RIS) zuständig.
    - Das RIS ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Es ist eine Datenbank, welche Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält.
    - Ein menschlicher Mitarbeiter kommt zu euch mit einer Nutzeranfrage/Frage, dessen Antworten sich in der Datenbank verstecken und ihr müsst die Frage so gut wie möglich beantworten.
    - Zur einfachen Durchsuchbarkeit wurden viele Daten durch ein Embeddingmodel als Vektoren embedded.
    - Du bist also Teil einer Retrieval Augmented Generation Anwendung.
    

    Ablauf:
    - Du bist der erste, der die Nutzeranfrage verarbeitet.
    - Eine Nutzeranfrage kann auf mehrere Themenbereiche abzielen und wenn der "Retriever"-Mitarbeiter eine Suche mit einem gemischten Themenbereich auf der Vektordatenbank durchführt, bekommt er sehr ungenaue Ergebnisse.
    - Deine Aufgabe ist es, die Nutzeranfrage in spezifischere, genauere, abzielendere Suchanfragen zu konvertieren.
    - Diese Suchanfragen können entweder Vektorsuchen sein oder Keywordsuchen.
        - Vektorsuchen: Diese sollten zwar spezifischer sein, aber trotzdem noch einen sehr guten Detailgrad haben und ganze Sätz sein.
        - Keywordsuchen: Diese sollten auf spezielle Keywords abzielen, welche auch gute Ergebnisse liefern könnten. Zum Beispiel eine Referenz auf ein Dokument oder ein Name einer Person. Längere Phrasen und Wörter, welche sowieso oft vorkommen, sollten vermieden werden, da diese keine Keywordsuche wert sind.
    - Gebe mindestens 1 Suchanfrage an und maximal 5 pro Typ.
    - Deine Antwort geht an den "Retriever"-Mitarbeiter, welcher dann die Daten mit einer Similarity-Search aus der Graphdatenbank holt.

    
    Aktuelles Datum und Uhrzeit: {formatted_current_datetime}


    Nutzeranfrage, welche du verarbeiten sollst:

    <Nutzeranfrage>
    {query}
    </Nutzeranfrage>
    """
    prompt_template = ChatPromptTemplate.from_template(prompt_template_string)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.25)
    structured_llm = llm.with_structured_output(SearchPlannerLlmDataModel)
    chain = (
        {
            "query": itemgetter("query"),
            "formatted_current_datetime": lambda x: datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            ),
        }
        | prompt_template
        | structured_llm
    )
    response: SearchPlannerLlmDataModel = chain.invoke(
        {
            "query": state.query,
        }
    )
    searches: list[SearchState] = []
    for x_vector_search_query in response.vector_search_querires:
        searches.append(
            SearchState(
                id=str(uuid.uuid4()),
                type=SearchType.VECTOR,
                query=x_vector_search_query,
            )
        )
    for x_keyword_search_query in response.keyword_search_queries:
        searches.append(
            SearchState(
                id=str(uuid.uuid4()),
                type=SearchType.KEYWORD,
                query=x_keyword_search_query,
            )
        )
    print(searches)
    return {"searches": searches}
