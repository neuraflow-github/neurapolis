from datetime import datetime
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from retriever.state.grading_state import GradingState
from retriever.state.hit_state import HitState
from retriever.state.hit_step import HitStep
from retriever.state.search_state import SearchState
from retriever.state.search_step import SearchStep
from retriever.utilities.generate_grading_llm_data_model import (
    generate_grading_llm_data_model,
)


def relevance_grader_node(search_state: SearchState):
    prompt_template_string = """ 
    Generell:
    - Du bist der "Relevance-Grader"-Mitarbeiter bei der deutschen Stadt Freiburg.
    - Du und deine Kollegen seid für das Rats Informations System (RIS) zuständig.
    - Das RIS ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Es ist eine Datenbank, welche Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält.
    - Ein menschlicher Mitarbeiter kommt zu euch mit einer Nutzeranfrage/Frage, dessen Antworten sich in der Datenbank verstecken und ihr müsst die Frage so gut wie möglich beantworten.
    - Zur einfachen Durchsuchbarkeit wurden viele Daten durch ein Embeddingmodel als Vektoren embedded.
    - Du bist also Teil einer Retrieval Augmented Generation Anwendung.
    
    Ablauf:
    - Du bekommst vom "Retriever"-Mitarbeiter einige Treffer aus der Datenbank, welche er relevant für die Nutzeranfrage hält.
    - Deine Aufgabe ist es, jeden der Treffer zu bewerten, ob dieser relevant für die Beantwortung der Nutzeranfrage sind oder nicht.
    - Behandle die Treffer von einander komplett unabhängig.
    - Sei dabei nicht zu streng, Treffer können auch nur teilweise relevant sein, oder entfernt über eine Verbindung relevant sein.
    - Wenn es also schon nur sehr sehr weit entfernt um das richtige Thema oder die richtigen Leute, Objekte, Gebäude oder Orte etc. geht, ist der Treffer relevant.
    - Treffer, welche du als irrelevant kennzeichnest, werdeb nicht zur Beantwortung der Nutzeranfrage zu Rate gezogen.
    
    Beispiele:
    - Nutzeranfrage 1: "Welche Projekte zur Stadtentwicklung wurden im letzten Quartal genehmigt?"
    - Treffer 1: "Beschlussvorlage zur Erweiterung des Stadtparks vom 10.09.2023..."
    - Antwort 1: "True" und "Relevant, da es sich um ein kürzlich genehmigtes Stadtentwicklungsprojekt handelt, das zur Beantwortung der Frage beitragen kann."

    - Nutzeranfrage 2: "Welche Maßnahmen wurden zur Verbesserung der Radwege beschlossen?"
    - Treffer 2: "Antrag zur Erhöhung der Hundesteuer..."
    - Antwort 2: "False" und "Irrelevant, da dies ein Antrag zur Hundesteuer ist und nichts mit Radwegen zu tun hat."

    - Nutzeranfrage 3: "Wer ist der aktuelle Oberbürgermeister von Freiburg?"
    - Treffer 3: "Lebenslauf von Martin Horn, Oberbürgermeister der Stadt Freiburg..."
    - Antwort 3: "True" und "Relevant, da es Informationen über den aktuellen Oberbürgermeister von Freiburg enthält."
    

    Aktuelles Datum und Uhrzeit: {formatted_current_datetime}


    Nutzeranfrage, welche du verarbeiten sollst:

    <Nutzeranfrage>
    {query}
    </Nutzeranfrage>


    Treffer, welche du verarbeiten sollst:

    {hits_xml}
    """
    prompt_template = ChatPromptTemplate.from_template(prompt_template_string)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.25)
    LlmDataModel = generate_grading_llm_data_model(len(search_state.hits))
    structured_llm = llm.with_structured_output(LlmDataModel)
    chain = (
        {
            "query": itemgetter("query"),
            "hits_xml": itemgetter("hits")
            | RunnableLambda(HitState.format_hits_to_inner_xml),
            "formatted_current_datetime": lambda x: datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            ),
        }
        | prompt_template
        | structured_llm
    )
    unique_hits = list(
        filter(
            lambda x_hit: x_hit.step == HitStep.FILE_SECTION_RETRIEVED,
            search_state.hits,
        )
    )
    if len(unique_hits) == 0:
        search_state.step = SearchStep.RELEVANCE_GRADED
        return {"searches": [search_state]}
    response = chain.invoke(
        {
            "query": search_state.query,
            "hits": unique_hits,
        }
    )
    for x_unique_hit_index, x_unique_hit in enumerate(unique_hits):
        for y_hit in search_state.hits:
            if y_hit.id != x_unique_hit.id:
                continue
            is_relevant = getattr(response, f"is_hit_{x_unique_hit_index+1}_relevant")
            feedback = getattr(response, f"hit_{x_unique_hit_index+1}_feedback")
            y_hit.grading = GradingState(
                is_relevant=is_relevant,
                feedback=feedback,
            )
            y_hit.step = HitStep.RELEVANCE_GRADED
    search_state.step = SearchStep.RELEVANCE_GRADED
    return {"searches": [search_state]}
