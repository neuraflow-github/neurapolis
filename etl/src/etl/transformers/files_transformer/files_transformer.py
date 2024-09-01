import logging
import os
import shutil
import uuid

from etl.models.file import File
from etl.services.db_session_builder import db_session_builder
from etl.utilities.config import config

from .file_reconstructor import FileReconstructor
from .file_sectionizer import FileSectionizer
from .file_sections_chunker import FileSectionsChunker
from .file_text_extractor import FileTextExtractor
from .file_uploader import FileUploader


class FilesTransformer:
    def __init__(self) -> None:
        self.file_text_extractor = FileTextExtractor()
        self.file_reconstructor = FileReconstructor()
        self.file_sectionizer = FileSectionizer()
        self.file_sections_chunker = FileSectionsChunker()
        self.file_uploader = FileUploader()

    def transform_files(self):
        # AND file.id = "https://ris.freiburg.de/oparl/file/sia%7C2024-HFA-87%7C1"
        with db_session_builder.build() as db_session:
            db_query = """
            MATCH (file:File)
            WHERE file.mime_type = "application/pdf"
            AND NOT EXISTS ((file)-[:FILE_HAS_FILE_SECTION]->())
            RETURN file
            ORDER BY file.id
            LIMIT $limit
            """
            while True:
                files_db_result = db_session.run(db_query, limit=1)
                files = []
                for x_file_db_dict in files_db_result:
                    file = File.from_db_dict(x_file_db_dict["file"])
                    files.append(file)
                for x_file in files:
                    logging.info(
                        f"{self.__class__.__name__}: Started transforming file {x_file.id}"
                    )
                    temp_file_dir_path = os.path.join(
                        config.temp_dir_path, str(uuid.uuid4())
                    )
                    os.makedirs(temp_file_dir_path, exist_ok=True)
                    self.file_text_extractor.extract_file_text(
                        x_file, temp_file_dir_path
                    )
                    self.file_reconstructor.reconstruct_file(x_file, temp_file_dir_path)
                    # temp_file_dir_path = "/Users/juliushuck/Projects/datas/ris/datastore/20_temp/4b8ff134-0c11-4953-af85-39524bd1c8a3"
                    self.file_sectionizer.sectionize_file(x_file, temp_file_dir_path)
                    self.file_sections_chunker.chunk_file(x_file, temp_file_dir_path)
                    self.file_uploader.upload_file(x_file, temp_file_dir_path)
                    shutil.rmtree(temp_file_dir_path)
                    logging.info(
                        f"{self.__class__.__name__}: Finished transforming file {x_file.id}"
                    )
