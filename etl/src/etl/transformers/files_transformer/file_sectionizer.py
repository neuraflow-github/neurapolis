import json
import logging
import os
import pickle
import uuid
from datetime import datetime
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field

from etl.models.file import File
from etl.models.file_section import FileSection


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
    splits: List[FileSectionizerLineSplitLlmDataModel] = Field(
        description="Liste der Aufteilungen",
        default=[],
    )


# Grund deiner Aufgabe:
# - Nach dir, werden die Sektionen noch jeweils in kleinere Textblöcke gechunkt und dann vektorembedded.
# - Später werden dem RIS dann verschiedene Fragen gestellt.
# - Um eine Frage zu beantworten wird eine Vektorsuche auf den Sektionen durchgeführt.
# - Diese wird einige Chunks zurückliefern. Von diesen Chunks retrieven wir dann die zugehörigen Sektionen (Parent-Document-Retrieval).
# - Die Sektionen werden dann an ein LLM gegeben, welches aufgrund dieser Texte dann eine Antwort auf die gestellte Frage genriert.
# - Manchmal enthalten Dokumente sehr unterschiedliche Themen. Damit der Context des LLMs nicht zugemüllt wird, wollen wir nicht immer das ganze Dokument mit in den Context geben.
# - Es macht Sinn das ganze Dokument mit rein zugeben, wenn es sich um "RELATED_TOPICS" handelt, da das ganze Dokument von einem großen Thema handelt.
# - Wenn es sich aber um "NOT_RELATED_TOPICS" handelt, dann sollte das LLM nur immer die bestimmte Sektion oder Sektionen des Dokuments bekommen, damit der Context nicht mit komplett irrelevanten Informationen zugemüllt wird.


class FileSectionizer:
    def __init__(self):
        self.prompt_template_string = """
        Du bist Teil einer Retrieval Augmented Generation Anwendung namens Rats Informations System (RIS). Du bist außerdem Teil der ETL-Pipeline dieser Anwendung.

        Das RIS ist eine Graphdatenbank, die Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält. Es ist ein internes System für Politiker und städtische Mitarbeiter, das ihnen bei ihrer Arbeit hilft. Deine Stadt ist die deutsche Stadt Freiburg.

        Die Aufgabe der ETL-Pipeline ist es, die Dateien für die Vektorsuche vorzubereiten, also Parsing, Bereinigung, Chunking, Embedding.

        Du bist der Datei-Sektionierer.

        Deine Aufgabe:
        - Schaue dir das angegebene Dokument genau an und finde heraus, um welchen der folgenden Inhaltstypen es sich handelt:
            - „NOT_RELATED_TOPICS": Dokument, welches mehrere Themen enthält, die nicht miteinander verwandt sind. Zum Beispiel Sitzungsprotokolle, bei denen es um sehr unterschiedliche Tagesordnungspunkte geht. Auch mehrere Bauanträge sind zum Beispiel alle nicht miteinander verwandt und sollten deswegen getrennt werden.
            - „RELATED_TOPICS": Dokument, welches sich mit einem bestimmten Thema befasst, vielleicht auch mit vielen Unterthemen, aber die meisten davon beziehen sich auf ein großes Thema.
            - „OTHER": Dokument, das weitere Analyse benötigt, weil es sich um ein Thema handelt, das nicht durch Text extrahiert werden kann. Zum Beispiel grafische Übersichten von Wahlergebnissen.
        - Antworte mit dem Inhaltstypen und einer kurzen Begründung, warum du diesen Typ ausgewählt hast.
        - Wenn es sich um den Inhaltstypen „NOT_RELATED_TOPICS" handelt, gib die Zeilennummern an, an denen das Dokument aufgeteilt werden sollte.
            - In jeder Sektion sollte es dann nur noch um ein größeres Thema gehen. Jede Sektion kann auch wieder mehere Themen beinhalten, aber diese sollten dann eher Unterthemen des größeren Themas sein.
            - Sektionen sollten also auch nicht viel zu klein schrittig werden.
            - Es wird immer vor der Zeile gesplittet. Wenn du also unter anderem Zeile 2 angibst, würde zwischen Zeile 1 und 2 gesplittet werden.
            - Gib zu jeder Aufteilung eine kurze Begründung an, warum du das Dokument an dieser Stelle aufgeteilt hast.

        <Inhalt des Dokuments>
        {document_content}
        </Inhalt des Dokuments>
        """
        self.prompt_template = ChatPromptTemplate.from_template(
            self.prompt_template_string
        )
        self.llm = AzureChatOpenAI(
            azure_deployment="gpt-4o",
            temperature=0,
            max_tokens=4096,
        )
        self.structured_output_llm = self.llm.with_structured_output(
            FileSectionizerLlmDataModel
        )
        self.chain = self.prompt_template | self.structured_output_llm

    def sectionize_file(self, file: File, temp_file_dir_path: str):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started sectionizing"
        )
        text_md_file_path = f"{temp_file_dir_path}/text.md"
        with open(text_md_file_path, "r") as text_md_file:
            file_text = text_md_file.read()
        logging.info(f"{self.__class__.__name__}: File: {file.id}: Started reasoning")
        chain_response = self.chain.invoke({"document_content": file_text})
        line_split_indices = []
        for x_split in chain_response.splits:
            line_split_indices.append(x_split.line_number)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished reasoning: Type: {chain_response.type}, Reason: {chain_response.reason}, Line split indices: {line_split_indices}"
        )
        sectionizer_result_pkl_file_path = os.path.join(
            temp_file_dir_path, "sectionizer_result.pkl"
        )
        with open(
            sectionizer_result_pkl_file_path, "wb"
        ) as sectionizer_result_pkl_file:
            pickle.dump(chain_response, sectionizer_result_pkl_file)
        sectionizer_result_json_file_path = os.path.join(
            temp_file_dir_path, "sectionizer_result.json"
        )
        with open(
            sectionizer_result_json_file_path, "w"
        ) as sectionizer_result_json_file:
            json.dump(
                {
                    "type": chain_response.type,
                    "reason": chain_response.reason,
                    "splits": [
                        {
                            "line_number": x_split.line_number,
                            "reason": x_split.reason,
                        }
                        for x_split in chain_response.splits
                    ],
                },
                sectionizer_result_json_file,
                indent=4,
                ensure_ascii=False,
            )
        file_sections = []
        if chain_response.type == "NOT_RELATED_TOPICS":
            new_file_sections = self._sectionize_file_text(
                file.id, file_text, line_split_indices
            )
            file_sections.extend(new_file_sections)
        elif chain_response.type == "RELATED_TOPICS":
            file_section = FileSection(
                id=str(uuid.uuid4()),
                file_id=file.id,
                text=file_text,
                created_at=datetime.now(),
                modified_at=datetime.now(),
            )
            file_sections.append(file_section)
        else:
            file_sections = []
        file_sections_pkl_file_path = os.path.join(
            temp_file_dir_path, "file_sections.pkl"
        )
        with open(file_sections_pkl_file_path, "wb") as file_sections_pkl_file:
            pickle.dump(file_sections, file_sections_pkl_file)
        file_sections_json_file_path = os.path.join(
            temp_file_dir_path, "file_sections.json"
        )
        file_section_dicts = []
        for x_file_section in file_sections:
            file_section_dicts.append(x_file_section.to_dict())
        with open(file_sections_json_file_path, "w") as file_sections_json_file:
            json.dump(
                file_section_dicts,
                file_sections_json_file,
                default=str,
                indent=4,
                ensure_ascii=False,
            )
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished sectionizing"
        )

    def _sectionize_file_text(
        self, file_id: str, file_text: str, split_lines: List[int]
    ) -> List[FileSection]:
        file_lines = file_text.splitlines()
        file_sections = []
        current_file_section = []
        for x_file_line_number, x_file_line in enumerate(file_lines, start=1):
            if x_file_line_number in split_lines:
                if current_file_section:
                    file_section = FileSection(
                        id=str(uuid.uuid4()),
                        file_id=file_id,
                        text="".join(current_file_section),
                        created_at=datetime.now(),
                        modified_at=datetime.now(),
                    )
                    file_sections.append(file_section)
                current_file_section = []
            current_file_section.append(x_file_line + "\n")
        if current_file_section:
            file_section = FileSection(
                id=str(uuid.uuid4()),
                file_id=file_id,
                text="".join(current_file_section),
                created_at=datetime.now(),
                modified_at=datetime.now(),
            )
            file_sections.append(file_section)
        return file_sections
