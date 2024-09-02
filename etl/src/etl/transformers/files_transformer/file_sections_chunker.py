import logging
import os
import pickle
import uuid
from datetime import datetime
from typing import List

from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from etl.models.file import File
from etl.models.file_chunk import FileChunk
from etl.models.file_section import FileSection


class FileSectionsChunker:
    def __init__(self):
        self.markdown_header_text_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
                ("####", "Header 4"),
                ("#####", "Header 5"),
                ("######", "Header 6"),
            ],
            strip_headers=False,
        )
        self.recursive_character_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        )

    def chunk_file(self, file: File, temp_file_dir_path: str):
        logging.info(f"{self.__class__.__name__}: File: {file.id}: Started chunking")
        file_sections_pkl_file_path = os.path.join(
            temp_file_dir_path, "file_sections.pkl"
        )
        with open(file_sections_pkl_file_path, "rb") as file_sections_pkl_file:
            file_sections: List[FileSection] = pickle.load(file_sections_pkl_file)
        file_chunks: List[FileChunk] = []
        for x_file_section in file_sections:
            markdown_header_text_splitter_chunk_texts = (
                self.markdown_header_text_splitter.split_text(x_file_section.text)
            )
            file_section_chunk_texts = []
            for (
                x_file_section_chunk_document
            ) in markdown_header_text_splitter_chunk_texts:
                recursive_character_text_splitter_chunk_texts = (
                    self.recursive_character_text_splitter.split_text(
                        x_file_section_chunk_document.page_content
                    )
                )
                file_section_chunk_texts.extend(
                    recursive_character_text_splitter_chunk_texts
                )
            for y_file_section_chunk_text in file_section_chunk_texts:
                file_chunk = FileChunk(
                    id=str(uuid.uuid4()),
                    file_section_id=x_file_section.id,
                    text=y_file_section_chunk_text,
                    created_at=datetime.now(),
                    modified_at=datetime.now(),
                )
                file_chunks.append(file_chunk)
        file_chunks_pkl_file_path = os.path.join(temp_file_dir_path, "file_chunks.pkl")
        with open(file_chunks_pkl_file_path, "wb") as file_chunks_pkl_file:
            pickle.dump(file_chunks, file_chunks_pkl_file)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished chunking: Found {len(file_chunks)} file chunks"
        )
