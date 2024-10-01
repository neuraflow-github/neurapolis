import os
from dotenv import load_dotenv
from langsmith import Client
from langsmith import evaluate
from langsmith.schemas import Example, Run
from pydantic import BaseModel, Field
import numpy as np
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

client = Client(api_key=os.environ["LANGCHAIN_API_KEY"], api_url=os.environ["LANGCHAIN_ENDPOINT"])
examples = list(client.list_examples(dataset_name="Neurapolis ETL Sectionizer"))

def evaluate_type(root_run: Run, example: Example) -> dict:
    outputs = root_run.outputs
    example_output = example.outputs
    return {
        "key": "type_comparison",
        "score": 1 if outputs['output'].type == example_output['type'] else 0,
    }

def calculate_splits_similarity(proposed_splits: list, golden_splits: list) -> float:
    # Calculate total lines
    total_lines = max(
        max(x_split.line_number for x_split in proposed_splits),
        max(y_split['line_number'] for y_split in golden_splits)
    )
    proposed = np.array([x_split.line_number for x_split in proposed_splits])
    golden = np.array([y_split['line_number'] for y_split in golden_splits])
    # Normalize the splits
    proposed_norm = proposed / total_lines
    golden_norm = golden / total_lines
    # Calculate the minimum distance for each proposed split to any golden split
    distances = np.min(np.abs(proposed_norm[:, np.newaxis] - golden_norm), axis=1)
    # Calculate similarity score (inverse of distance)
    similarities = 1 / (1 + distances)
    return np.mean(similarities)

def evaluate_splits(root_run: Run, example: Example) -> dict:
    outputs = root_run.outputs['output']
    example_output = example.outputs
    if outputs.type == "OTHER" or example_output['type'] == "OTHER":
        return {
            "key": "splits_comparison",
            "score": None,
            "metadata": {
                "reason": "Type is OTHER, so no splits are needed."
            }
        }
    proposed_splits = outputs.splits
    golden_splits = example_output['splits']
    similarity = calculate_splits_similarity(proposed_splits, golden_splits)
    return {
        "key": "splits_comparison",
        "score": similarity,
        "metadata": {
            "proposed_splits": [x_split.line_number for x_split in proposed_splits],
            "golden_splits": [y_split['line_number'] for y_split in golden_splits],
        }
    }

def evaluate_split_count(root_run: Run, example: Example) -> dict:
    outputs = root_run.outputs['output']
    example_output = example.outputs
    if outputs.type != 'NOT_RELATED_TOPICS' or example_output['type'] != 'NOT_RELATED_TOPICS':
        return {
            "key": "split_count_comparison",
            "score": None,  # No score for non-NOT_RELATED_TOPICS types
            "metadata": {
                "count_match": "N/A",
                "reason": "Not applicable for this document type"
            }
        }
    proposed_splits = outputs.splits
    golden_splits = example_output['splits']
    proposed_count = len(proposed_splits)
    golden_count = len(golden_splits)
    # Calculate the difference in counts
    count_difference = abs(proposed_count - golden_count)
    # Normalize the score based on the difference
    max_difference = max(proposed_count, golden_count)
    score = 1 - (count_difference / max_difference) if max_difference > 0 else 1
    return {
        "key": "split_count_comparison",
        "score": score,
        "metadata": {
            "proposed_count": proposed_count,
            "golden_count": golden_count,
            "count_difference": count_difference
        }
    }

def compound_metric(root_run: Run, example: Example) -> dict:
    type_score = evaluate_type(root_run, example)['score']
    splits_result = evaluate_splits(root_run, example)
    count_result = evaluate_split_count(root_run, example)
    splits_score = splits_result['score']
    count_score = count_result['score']
    # If the type is not NOT_RELATED_TOPICS, only consider the type score
    if splits_score is None or count_score is None:
        compound_score = type_score
        reason = "Only type comparison applicable"
    else:
        # Combine scores (you can adjust the weights as needed)
        compound_score = 0.4 * type_score + 0.3 * splits_score + 0.3 * count_score
        reason = "All metrics applicable"
    return {
        "key": "compound_metric",
        "score": compound_score,
        "metadata": {
            "type_score": type_score,
            "splits_score": splits_score,
            "count_score": count_score,
            "reason": reason
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
    reason: str = Field(
        description="Kurze Begründung für die Entscheidung des Inhaltstyps"
    )
    splits: list[FileSectionizerLineSplitLlmDataModel] = Field(
        description="Liste der Aufteilungen",
        default_factory=lambda: [FileSectionizerLineSplitLlmDataModel(line_number=1, reason="Start der ersten Sektion")]
    )

prompt_template_string = """
- !!! Antworte immer in dem gegebenen Format. !!!
Du bist Teil einer Retrieval Augmented Generation Anwendung namens Rats Informations System (RIS). Du bist außerdem Teil der ETL-Pipeline dieser Anwendung.

Das RIS ist eine Datenbank, die Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält. Es ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Deine Stadt ist die deutsche Stadt Freiburg.

Die Aufgabe der ETL-Pipeline ist es, die Dateien für die Vektorsuche vorzubereiten, also Parsing, Bereinigung, Chunking, Embedding.

Du bist der Datei-Sektionierer.

Deine Aufgabe:
- Schaue dir das angegebene Dokument genau an und finde heraus, um welchen der folgenden Inhaltstypen es sich handelt:
    - "NOT_RELATED_TOPICS": Dokument, welches mehrere Themen enthält, die nicht miteinander verwandt sind. Zum Beispiel Sitzungsprotokolle, bei denen es um sehr unterschiedliche Tagesordnungspunkte geht. Auch mehrere Bauanträge sind zum Beispiel alle nicht miteinander verwandt und sollten deswegen getrennt werden.
    - "RELATED_TOPICS": Dokument, welches sich mit einem bestimmten Thema befasst, vielleicht auch mit vielen Unterthemen, aber die meisten davon beziehen sich auf ein großes Thema.
    - "OTHER": Dokument, das weitere Analyse benötigt, weil es sich um ein Thema handelt, das nicht durch Text extrahiert werden kann. Zum Beispiel Dokumente, welche nur eine Grafik oder Bild enthalten, grafische Übersichten von Wahlergebnissen oder Kalendar. Aber auch Dokumente, welche nur eine große Finanztabelle enthalten, etc. Zähle zu diesen Dokumenten aber auch noch einenn weiteren Dokumenttypen hinzu: Einladungen zu einem Meeting, welche hauptsählich eine Einladung sind, welche noch die Tagesordungspunkte enthalten, sind auch "OTHER", da diese später anders verarbeitet werden.
- Antworte mit dem Inhaltstypen und einer kurzen Begründung, warum du diesen Typ ausgewählt hast.
- Wenn es sich um den Inhaltstypen "NOT_RELATED_TOPICS" oder "RELATED_TOPICS" handelt, gib die Zeilennummern an, an denen das Dokument aufgeteilt werden sollte.
    - In jeder Sektion sollte es dann nur noch um ein Thema gehen.
    - Sektionen sollten also nicht viel zu klein schrittig werden.
    - Es wird immer vor der Zeile gesplittet. Wenn du also unter anderem die Zeilennummer 2 angibst, würde zwischen Zeile 1 und 2 gesplittet werden.
    - Gib zu jeder Aufteilung eine kurze Begründung an, warum du das Dokument an dieser Stelle aufgeteilt hast.

Achtung:
- Oft enthalten die Dokumente auch Seitennummern, verwechsle diese nicht mit Aufzählungen.
- Tagesordnungspunkt wird oft mit "TOP" abgekürzt.
- Fange kein Pattern an, also nicht zb einfach alle 10 Zeilen splitten.
- Gebe immer die Zeilennummer 1 als erste Aufteilung aus, egal um welchen Typen es sich handelt.
- !!! Antworte immer in dem gegebenen Format. !!!


Beispiele:
- Ein Dokument handelt von dem Bau einer neuen Autobahn. In dem Dokument werden viele Themen beleuchtet. Teile das Dokument dann zum Beispiel in Sektionen wie "Umweltbelastung", "Einfluss auf die Tierwelt", "Baustand", etc, wenn die einzelnen Sektionen schon ziemlich lang sind.
- Ein Dokument ist ein Protokoll einer Sitzung. In der Sitzung ging es nur kurz um einige Aspekte eines Spielplatzes. Teile das Dokument nicht unbedingt in die Aspekte auf, wenn es nur kurz um diese Ding und es eigentlich ein großes Thema ist.
- Ein Dokument ist ein Protokoll einer Sitzung. Die Sitzung war ein reguläres Meeting, in welchem es um unterschiedliche Themen ging. Teile das Dokument in Sektionen, wie "Bauantrag 1", "Bauantrag 2", "Vortrag 1", "Vortrag 2", "Bürgerstimmen", "Entscheidung bzgl. Spielplatz", etc.

<Dokument>
{text}
</Dokument>
- !!! Antworte immer in dem gegebenen Format. !!!
"""
prompt_template = PromptTemplate.from_template(prompt_template_string)
llm = AzureChatOpenAI(deployment_name="gpt-4o")
structured_llm = llm.with_structured_output(FileSectionizerLlmDataModel)
chain = prompt_template | structured_llm
result = evaluate(
    lambda x: chain.invoke(x["text_lines"]),
    data=examples,
    evaluators=[evaluate_type, evaluate_splits, evaluate_split_count, compound_metric],
    experiment_prefix="example",
    client=client
)