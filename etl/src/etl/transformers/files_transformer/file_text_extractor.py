import json
import logging
import os

import requests
import yaml
from PyPDF2 import PdfReader, PdfWriter

from etl.models.file import File
from etl.utilities.config import config


class FileTextExtractor:
    def extract_file_text(self, file: File, temp_file_dir_path: str):
        logging.info(
            f"{self.__class__.__name__}: Started extracting text of file {file.id}"
        )
        file_pdf_file_path = os.path.join(temp_file_dir_path, "file.pdf")
        metadata_file_path = os.path.join(temp_file_dir_path, "metadata.json")
        with open(metadata_file_path, "w") as metadata_file:
            json.dump(
                file.to_db_dict(),
                metadata_file,
                indent=4,
                ensure_ascii=False,
            )
        page_request_response = requests.get(file.download_url)
        page_request_response.raise_for_status()
        with open(file_pdf_file_path, "wb") as file_pdf:
            file_pdf.write(page_request_response.content)
        pages_dir_path = os.path.join(temp_file_dir_path, "pages")
        os.makedirs(pages_dir_path, exist_ok=True)
        pdf_reader = PdfReader(file_pdf_file_path)
        for page_index in range(len(pdf_reader.pages)):
            logging.info(
                f"{self.__class__.__name__}: Started extracting text of page {page_index} of file {file.id}"
            )
            page_dir_path = os.path.join(pages_dir_path, str(page_index))
            os.makedirs(page_dir_path, exist_ok=True)
            page_file_path = os.path.join(page_dir_path, "page.pdf")
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_index])
            with open(page_file_path, "wb") as file_page_file:
                pdf_writer.write(file_page_file)
            with open(page_file_path, "rb") as file_page_file:
                page_request_response = requests.post(
                    config.unstructured_api_url + "/extract-document",
                    files={"file": file_page_file},
                )
            page_request_response.raise_for_status()
            text_elements_yaml_file_path = os.path.join(
                page_dir_path, "text_elements.yaml"
            )
            with open(text_elements_yaml_file_path, "w") as text_elements_yaml_file:
                yaml.dump(page_request_response.json(), text_elements_yaml_file)
            logging.info(
                f"{self.__class__.__name__}: Finished extracting text of page {page_index} of file {file.id}"
            )
        logging.info(
            f"{self.__class__.__name__}: Finished extracting text of file {file.id}"
        )
