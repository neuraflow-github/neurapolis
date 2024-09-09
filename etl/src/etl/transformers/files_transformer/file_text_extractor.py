import json
import logging
import os

import requests
import yaml
from PyPDF2 import PdfReader, PdfWriter

from etl.config import config
from etl.models.file import File

from .file_uploader import FileUploader


class FileTextExtractor:
    def extract_file_text(self, file: File, temp_file_dir_path: str):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started extracting file text"
        )
        file_pdf_file_path = os.path.join(temp_file_dir_path, "file.pdf")
        metadata_json_file_path = os.path.join(temp_file_dir_path, "metadata.json")
        with open(metadata_json_file_path, "w") as metadata_json_file:
            json.dump(
                file.to_db_dict(),
                metadata_json_file,
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
        page_count = len(pdf_reader.pages)
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Found {page_count} pages"
        )
        if page_count > 20:
            logging.error(
                f"{self.__class__.__name__}: File: {file.id}: Found {page_count} pages. This is too many pages to extract text from."
            )
            FileUploader().set_file_page_count(file, page_count)
            raise Exception(
                f"{self.__class__.__name__}: File: {file.id}: Found {page_count} pages. This is too many pages to extract text from."
            )
        for page_index in range(page_count):
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_index}: Started extracting page text"
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
                    "https://api.unstructuredapp.io/general/v0/general",
                    headers={
                        "accept": "application/json",
                        "Content-Type": "multipart/form-data",
                        "unstructured-api-key": "7LrPgi78ECkbH5cLQ1PHFYYlAtKdOL",
                    },
                    files={"files": file_page_file},
                    timeout=30,
                )
            page_request_response.raise_for_status()
            page_request_json = page_request_response.json()
            print(page_request_json)
            raise Exception("test")
            text_elements_yaml_file_path = os.path.join(
                page_dir_path, "text_elements.yaml"
            )
            with open(text_elements_yaml_file_path, "w") as text_elements_yaml_file:
                yaml.dump(page_request_response.json(), text_elements_yaml_file)
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_index}: Finished extracting page text"
            )
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished extracting file text"
        )
