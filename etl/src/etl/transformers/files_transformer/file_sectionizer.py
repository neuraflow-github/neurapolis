import logging
import os
import pickle
import uuid
from datetime import datetime
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from etl.models.file import File
from etl.models.file_section import FileSection


class FileSectionizerLlmDataModel(BaseModel):
    type: str = Field(description="Der Inhaltstyp des Dokuments")
    line_split_indices: List[int] = Field(
        description="Zeilennummern zum Aufteilen des Dokuments", default=[]
    )
    reason: str = Field(description="Begründung für die Entscheidung")


class FileSectionizer:
    def __init__(self):
        self.prompt_template_string = """
        Du bist Teil einer Retrieval Augmented Generation Anwendung namens Rats Informations System (RIS). Du bist außerdem Teil der ETL-Pipeline dieser Anwendung.

        Das RIS ist eine Graphdatenbank, die Informationen einer bestimmten Stadt über Organisationen, Personen, Sitzungen, Dateien usw. enthält. Es ist ein internes System für Politiker, das ihnen bei ihrer Arbeit hilft. Deine Stadt ist die deutsche Stadt Freiburg.

        Die Aufgabe der ETL-Pipeline ist es, die Dateien für die Vektorsuche vorzubereiten, also Parsing, Bereinigung, Chunking, Embedding.

        Du bist der Datei-Inhalts-Kategorie-Prüfer.

        Deine Aufgabe:
        - Schaue dir das gegebene Dokument genau an und finde heraus, um welchen der folgenden Inhaltstypen es sich handelt:
            - „NOT_RELATED_TOPICS": Dokument, das mehrere Themen enthält, die nicht miteinander verwandt sind. Oft Sitzungsprotokolle, bei denen es sehr unterschiedliche Tagesordnungspunkte gab.
            - „RELATED_TOPICS": Dokument, das sich mit einem bestimmten Thema befasst, vielleicht auch mit vielen Unterthemen, aber die meisten davon beziehen sich auf ein großes Thema.
            - „OTHER": Dokument, das weitere Analyse benötigt, weil es sich um ein Thema handelt, das nicht durch Text extrahiert werden kann. Manchmal Wahlergebnisse usw.
        - Antworte mit der Dateiinhaltskategorie und einer kurzen Begründung, warum du das denkst.
        - Wenn es sich um „NOT_RELATED_TOPICS" handelt, gib die Zeilennummern an, an denen das Dokument aufgeteilt werden sollte. Es wird immer vor der Zeile gesplittet. Wenn du also unter anderem Zeile 2 angibst, würde zwischen Zeile 1 und 2 gesplittet werden.

        Gib deine Antwort in dem strukturierten Format aus.

        Hier ist der Inhalt des Dokuments:

        <Inhalt des Dokuments>
        {document_content}
        </Inhalt des Dokuments>
        """
        self.prompt_template = ChatPromptTemplate.from_template(
            self.prompt_template_string
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.structured_llm = self.llm.with_structured_output(
            FileSectionizerLlmDataModel
        )
        self.chain = self.prompt_template | self.structured_llm

    def sectionize_file(self, file: File, temp_file_dir_path: str):
        logging.info(f"{self.__class__.__name__}: Started sectionizing file {file.id}")
        text_md_file_path = f"{temp_file_dir_path}/text.md"
        with open(text_md_file_path, "r") as text_md_file:
            file_text = text_md_file.read()
        logging.info(f"{self.__class__.__name__}: Started reasoning file {file.id}")
        chain_response = self.chain.invoke({"document_content": file_text})
        logging.info(
            f"{self.__class__.__name__}: Finished reasoning file {file.id}. Type: {chain_response.type}, Reason: {chain_response.reason}, Line split indices: {chain_response.line_split_indices}"
        )
        sectionizer_result_pkl_file_path = os.path.join(
            temp_file_dir_path, "sectionizer_result.pkl"
        )
        with open(
            sectionizer_result_pkl_file_path, "wb"
        ) as sectionizer_result_pkl_file:
            pickle.dump(chain_response, sectionizer_result_pkl_file)
        file_sections = []
        if chain_response.type == "NOT_RELATED_TOPICS":
            new_file_sections = self._sectionize_file_text(
                file.id, file_text, chain_response.line_split_indices
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
        logging.info(f"{self.__class__.__name__}: Finished sectionizing file {file.id}")

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
