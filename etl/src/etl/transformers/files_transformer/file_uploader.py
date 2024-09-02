import logging
import os
import pickle
from typing import List

from etl.models.file import File
from etl.models.file_chunk import FileChunk
from etl.models.file_section import FileSection
from etl.services.db_session_builder import db_session_builder

from .file_sectionizer import FileSectionizerLlmDataModel


class FileUploader:
    def upload_file(
        self,
        file: File,
        temp_file_dir_path: str,
    ):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started uploading file"
        )
        text_md_file_path = os.path.join(temp_file_dir_path, "text.md")
        with open(text_md_file_path, "r") as text_md_file:
            text = text_md_file.read()
        sectionizer_result_pkl_file_path = os.path.join(
            temp_file_dir_path, "sectionizer_result.pkl"
        )
        with open(
            sectionizer_result_pkl_file_path, "rb"
        ) as sectionizer_result_pkl_file:
            sectionizer_result: FileSectionizerLlmDataModel = pickle.load(
                sectionizer_result_pkl_file
            )
        self.update_file(
            file,
            text,
            sectionizer_result.type,
            sectionizer_result.reason,
        )
        file_sections_pkl_file_path = os.path.join(
            temp_file_dir_path, "file_sections.pkl"
        )
        with open(file_sections_pkl_file_path, "rb") as file_sections_pkl_file:
            file_sections = pickle.load(file_sections_pkl_file)
        self.upload_file_sections(file, file_sections)
        self.upload_file_has_file_section_relationships(file, file_sections)
        file_chunks_pkl_file_path = os.path.join(temp_file_dir_path, "file_chunks.pkl")
        with open(file_chunks_pkl_file_path, "rb") as file_chunks_pkl_file:
            file_chunks = pickle.load(file_chunks_pkl_file)
        self.upload_file_chunks(file, file_chunks)
        self.upload_file_section_has_file_chunk_relationships(file, file_chunks)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished uploading file"
        )

    def update_file(
        self, file: File, text: str, sectionizer_type: str, sectionizer_reason: str
    ):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started updating file"
        )
        db_query = """
        MATCH (file_node:File {id: $file_id})
        SET file_node.extracted_text = $extracted_text,
            file_node.sectionizer_type = $sectionizer_type,
            file_node.sectionizer_reason = $sectionizer_reason
        """
        with db_session_builder.build() as db_session:
            db_session.run(
                db_query,
                file_id=file.id,
                extracted_text=text,
                sectionizer_type=sectionizer_type,
                sectionizer_reason=sectionizer_reason,
            )
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished updating file"
        )

    def upload_file_sections(self, file: File, file_sections: List[FileSection]):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started uploading file sections"
        )
        db_query = """
        UNWIND $file_section_db_dicts AS x_file_section_db_dict
        MERGE (file_section_node:FileSection {id: x_file_section_db_dict.id})
        SET file_section_node += x_file_section_db_dict
        """
        file_section_db_dicts = []
        for file_section in file_sections:
            file_section_db_dict = file_section.to_db_dict()
            file_section_db_dicts.append(file_section_db_dict)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Found {len(file_section_db_dicts)} file sections"
        )
        with db_session_builder.build() as db_session:
            db_session.run(db_query, file_section_db_dicts=file_section_db_dicts)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished uploading file sections"
        )

    def upload_file_has_file_section_relationships(
        self, file: File, file_sections: List[FileSection]
    ):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started uploading FILE_HAS_FILE_SECTION relationships"
        )
        db_query = """
        UNWIND $pairs AS relationship_pair
        MATCH (file_node:File {id: relationship_pair.start_id})
        MATCH (file_section_node:FileSection {id: relationship_pair.end_id})
        MERGE (file_node)-[:FILE_HAS_FILE_SECTION]->(file_section_node)
        """
        pairs = []
        for file_section in file_sections:
            pair = {
                "start_id": file_section.file_id,
                "end_id": file_section.id,
            }
            pairs.append(pair)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Found {len(pairs)} FILE_HAS_FILE_SECTION relationships"
        )
        with db_session_builder.build() as db_session:
            db_session.run(db_query, pairs=pairs)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished uploading FILE_HAS_FILE_SECTION relationships"
        )

    def upload_file_chunks(self, file: File, file_chunks: List[FileChunk]):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started uploading file chunks"
        )
        db_query = """
        UNWIND $file_chunk_db_dicts AS x_file_chunk_db_dict
        MERGE (file_chunk_node:FileChunk {id: x_file_chunk_db_dict.id})
        SET file_chunk_node += x_file_chunk_db_dict
        """
        file_chunk_db_dicts = []
        for file_chunk in file_chunks:
            file_chunk_db_dicts.append(file_chunk.to_db_dict())
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Found {len(file_chunk_db_dicts)} file chunks"
        )
        with db_session_builder.build() as db_session:
            db_session.run(db_query, file_chunk_db_dicts=file_chunk_db_dicts)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished uploading file chunks"
        )

    def upload_file_section_has_file_chunk_relationships(
        self, file: File, file_chunks: List[FileChunk]
    ):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started uploading FILE_SECTION_HAS_FILE_CHUNK relationships"
        )
        db_query = """
        UNWIND $pairs AS relationship_pair
        MATCH (file_section_node:FileSection {id: relationship_pair.start_id})
        MATCH (file_chunk_node:FileChunk {id: relationship_pair.end_id})
        MERGE (file_section_node)-[:FILE_SECTION_HAS_FILE_CHUNK]->(file_chunk_node)
        """
        pairs = []
        for file_chunk in file_chunks:
            pair = {
                "start_id": file_chunk.file_section_id,
                "end_id": file_chunk.id,
            }
            pairs.append(pair)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Found {len(pairs)} FILE_SECTION_HAS_FILE_CHUNK relationships"
        )
        with db_session_builder.build() as db_session:
            db_session.run(db_query, pairs=pairs)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished uploading FILE_SECTION_HAS_FILE_CHUNK relationships"
        )
