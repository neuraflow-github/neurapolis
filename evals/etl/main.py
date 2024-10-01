import os
from dotenv import load_dotenv
from langsmith import Client
from langsmith import evaluate
from langsmith.schemas import Example, Run
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

client = Client(api_key=os.environ["LANGCHAIN_API_KEY"], api_url=os.environ["LANGCHAIN_ENDPOINT"])
examples = list(client.list_examples(dataset_name="Neurapolis ETL Sectionizer"))

def evaluate_type(root_run: Run, example: Example) -> dict:
    proposed_outputs = root_run.outputs["output"]
    example_output = example.outputs
    return {
        "key": "type_comparison",
        "score": 1 if proposed_outputs.type == example_output["type"] else 0,
    }

def calculate_error_margins(golden_splits):
    error_margins = []
    for x_index in range(len(golden_splits)):
        if x_index == 0:
            prev_split = 0
            next_split = golden_splits[1] if len(golden_splits) > 1 else float('inf')
        elif x_index == len(golden_splits) - 1:
            prev_split = golden_splits[x_index - 1]
            next_split = float('inf')
        else:
            prev_split = golden_splits[x_index - 1]
            next_split = golden_splits[x_index + 1]
        distance_to_next = next_split - golden_splits[x_index]
        distance_to_prev = golden_splits[x_index] - prev_split
        distance = min(distance_to_next, distance_to_prev)
        if distance <= 5:
            error_margins.append(1)
        elif distance <= 10:
            error_margins.append(2)
        else:
            error_margins.append(3)
    
    return error_margins

def evaluate_split_similarity(root_run: Run, example: Example) -> dict:
    proposed_outputs = root_run.outputs["output"]
    example_output = example.outputs
    if proposed_outputs.type == "OTHER" or example_output["type"] == "OTHER":
        return {
            "key": "split_similarity",
            "score": None,  # No score
            "metadata": {
                "reason": "Type is OTHER, so no splits are needed."
            }
        }
    proposed_split_line_numbers = [split.line_number for split in proposed_outputs.splits]
    golden_split_line_numbers = [split["line_number"] for split in example_output["splits"]]
    error_margins = calculate_error_margins(golden_split_line_numbers)
    hit_count = 0
    for x_proposed_split_line_number in proposed_split_line_numbers:
        for y_golden_split_line_number, y_error_margin in zip(golden_split_line_numbers, error_margins):
            if abs(x_proposed_split_line_number - y_golden_split_line_number) <= y_error_margin:
                hit_count += 1
                break
    total_golden_splits = len(golden_split_line_numbers)
    total_proposed_splits = len(proposed_split_line_numbers)
    
    precision = hit_count / total_proposed_splits
    recall = hit_count / total_golden_splits
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return {
        "key": "split_similarity",
        "score": f1_score,
        "metadata": {
            "proposed_splits": proposed_split_line_numbers,
            "golden_splits": golden_split_line_numbers,
            "total_proposed_splits": total_proposed_splits,
            "total_golden_splits": total_golden_splits,
            "error_margins": error_margins,
            "hit_count": hit_count,
            "precision": precision,
            "recall": recall
        }
    }

def compound_metric(root_run: Run, example: Example) -> dict:
    proposed_outputs = root_run.outputs["output"]
    example_output = example.outputs
    type_score = evaluate_type(root_run, example)["score"]
    split_similarity_score = evaluate_split_similarity(root_run, example)["score"]
    compound_score = None
    if proposed_outputs.type == "OTHER" or example_output["type"] == "OTHER":
        compound_score = type_score
    else:
        compound_score = 0.3 * type_score + 0.7 * split_similarity_score
    return {
        "key": "compound_metric",
        "score": compound_score,
        "metadata": {
            "type_score": type_score,
            "split_similarity_score": split_similarity_score,
        }
    }

class FileSectionizerLineSplitLlmDataModel(BaseModel):
    line_number: int = Field(
        description="Zeilennummer, an der das Dokument aufgeteilt werden soll"
    )
    reason: str = Field(
        description="Kurze Begründung für die Aufteilung an dieser Stelle"
    )

class FileSectionizerLlmDataModel(BaseModel):
    type: str = Field(description="Der Inhaltstyp des Dokuments")
    type_reason: str = Field(
        description="Kurze Begründung für die Entscheidung des Inhaltstyps"
    )
    splits: list[FileSectionizerLineSplitLlmDataModel] = Field(
        description="Liste der Aufteilungen",
        default_factory=lambda: [FileSectionizerLineSplitLlmDataModel(line_number=1, reason="Start der ersten Sektion")]
    )

prompt_template_string = """
Du bist Teil einer Retrieval Augmented Generation Anwendung namens Rats Informations System (RIS). Du bist außerdem Teil der ETL-Pipeline dieser Anwendung.

Das RIS ist eine Datenbank, die Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält. Es ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Deine Stadt ist die deutsche Stadt Freiburg.

Die Aufgabe der ETL-Pipeline ist es, die Dateien für die Vektorsuche vorzubereiten, also Parsing, Bereinigung, Chunking, Embedding.

Du bist der Datei-Sektionierer.

Deine Aufgabe:
- Schaue dir das angegebene Dokument genau an und finde heraus, um welchen der folgenden Typen es sich handelt:
    - "OTHER": Dokument, welches weitere Analyse benötigt, weil es sich um ein Thema handelt, das nicht durch Text extrahiert werden kann. Zum Beispiel Dokumente, welche nur eine Grafik oder Bild enthalten, grafische Übersichten von Wahlergebnissen oder Kalendar. Auch Dokumente welche sehr, sehr viel unleserlichen Text enthalten (oftmals in sehr sehr schlecht extrahierten Tabellen). Aber auch Dokumente, welche nur oder hauptsächlich eine große Finanztabelle enthalten. Zähle als "OTHER" aber auch noch Einladungen (mit oft Tagesordnungspunkten) oder Absagen von Sitzungen oder Agendas von Sitzungen, welche nicht die Ergebnisse der Sitzung enthalten.
    - "STANDARD": Alle Dokumente, welche nicht als "OTHER" klassifiziert werden können. Manche Dokumente enthalten Tabellen, haben aber trotzdem noch viel textlichen Inhalt zu oder in der Tabelle und zählen dann auf jeden Fall als "STANDARD". Nur wenn der Text in den Tabellen extrem unleserlich ist oder hauptsächlich Zahlen sind, dann zählt das Dokument als "OTHER". Ergebnismitteilungen von Sitzungen zählen als "STANDARD".
- Antworte mit dem Typen und einer kurzen Begründung, warum das Dokument diesen Typ hat.
- Wenn es sich um den Typen "STANDARD" handelt, gib die Aufteilungen an, an denen das Dokument in Sektionen aufgeteilt werden sollte.
    - Dokumente behandeln oft nur ein einziges Thema. In diesen Fällen muss das Dokument nur in mehrere Sektionen aufgeteilt werden, wenn es sehr sehr lang ist, zum Beispiel länger als 4 Seiten/150 Zeilen mit sehr viel Text. Ansonsten reicht eine Sektion auf Zeilennummer 1.
    - Solche zusammenhängende Dokumente müssen also nur extrem selten aufgeteilt werden.
    - Es ist auch kein Problem, wenn es in dem Dokument um meherere Unterprojekte oder Unterthemen zu dem großen Thema geht.
    - Manche Dokumente (oftmals Sitzungsprotokolle) bestehen aber aus sehr unterschiedlichen Themen, welche unabhängig voneinander sind. Zum Beispiel einzelne Tagesordungspunkte oder Bauanträge. In diesem Fall sollte das Dokument in Sektionen aufgeteilt werden, wobei jedes Thema eine eigene Sektion ist.
    - Siehe die unteren Beispiele, für ein intuitiveres Verständnis.
    - Sektionen sollten auf keinen Fall zu kleinschrittig werden.
    - Es wird immer vor der Zeile gesplittet. Wenn du also unter anderem die Zeilennummer 2 angibst, würde zwischen Zeile 1 und 2 gesplittet werden.
    - Gib zu jeder Aufteilung eine kurze Begründung an, warum das Dokument an dieser Stelle aufgeteilt werden sollte.

Achtung:
- Oft enthalten die Dokumente auch Seitennummern, verwechsle diese nicht mit Aufzählungen.
- Tagesordnungspunkt wird oft mit "TOP" abgekürzt.
- Fange kein Pattern an, also nicht zb einfach alle 10 Zeilen splitten.
- Das Limit für eine Sektion ist etwa 4 Seiten/150 volle Zeilen. Tabellen, Überschriften, sehr kurze Texte zählen aber nicht als volle Zeilen. Eine Sektion kann also schon sehr sehr lang sein.
- Manchmal hat ein Tagesordungspunkt eine kurze Einleitung und dann gibt es einen Unterpunkt, welcher relativ unabhängig ist. In diesem Fall sollte es eine Sektion für die Einleitung geben und dann für den oder die unabhängigen Unterpunkte.
- Gebe immer die Zeilennummer 1 als erste Aufteilung aus, egal um welchen Typen es sich handelt.


Beispiele:
- Ein Dokument handelt von dem Bau einer neuen Autobahn. In dem Dokument werden viele Unterthemen sehr detailliert beleuchtet. Teile das Dokument in Sektionen wie "Umweltbelastung", "Einfluss auf die Tierwelt", "Baustand", etc.
- Ein Dokument ist ein Protokoll einer Sitzung. In der Sitzung ging es um einige Aspekte eines Spielplatzes. Die einzelnen Aspekte wurden aber nicht sehr sehr ausgiebig beleuchtet. Teile das Dokument nur in eine zusammenhängende Sektion.
- Ein Dokument ist ein Protokoll einer Sitzung. Die Sitzung war ein reguläres Meeting, in welchem es um unterschiedliche Themen ging. Teile das Dokument in Sektionen, wie "Einleitung", "Abstimmung zu X", "Einleitung Bauanträge", "Bauantrag 1", "Bauantrag 2", "Vortrag 1", "Vortrag 2", "Bürgerstimmen", "Entscheidung bzgl. Spielplatz", etc.

<Dokument>
{text}
</Dokument>

Antworte immer in dem angegebenen Format.
"""
prompt_template = PromptTemplate.from_template(prompt_template_string)
llm = AzureChatOpenAI(deployment_name="gpt-4o", temperature=0)
structured_llm = llm.with_structured_output(FileSectionizerLlmDataModel)
chain = prompt_template | structured_llm
result = evaluate(
    lambda x: chain.invoke(x["text_lines"]),
    data=examples,
    evaluators=[evaluate_type, evaluate_split_similarity, compound_metric],
    experiment_prefix="example",
    client=client
)