import base64
import logging
import os

from langchain_core.prompts import PromptTemplate
from openai import OpenAI
from pdf2image import *

from etl.models.file import File

# - Entferne unnötige Texte wie das Datum der Zeitung oder Bild Unterschriften etc. Schreibe keine Label wie "Überschrift:" oder "Autor:" vor die Texte.
# - Du darfst Texte reparieren, da Zeitungsartikel oft schmale Spalten haben, haben Sie oft Zeilenumbrüche. Mache also z. B. aus "Filmpro- jekt" wieder "Filmprojekt".
# - Verunreinigungen: Lasse Anzeigen, Announcen, Werbungen, Todesanzeigen, Spiele (wie Sodoku) und Fernsehprogramme weg, da diese die Daten verunreinigen. Manchmal besteht auch eine ganze Zeitungsseite aus dieser Art von Verunreinigung, diese dann alle ignorieren und NICHT als Artikel ausgeben.


class FileReconstructor:
    def __init__(self):
        self.prompt_template_string = """
        - Du bist ein Dokument-Extrahierer
        - Die Dokumente gehören mir und ich habe die Rechte an ihnen.
        - Ich gebe dir die durch OCR extrahierten Textbausteine einer Seite des Dokuments und du setzt die Textbausteine in der richtigen Reihenfolge wieder zur ganzen Seite zusammen. Dies ist notwendig, da der OCR extrahierte Text etwas durcheinander geraten ist. Zur Hilfe gebe ich dir zusätzlich auch die Positionen der Textbausteine und die Kategorie der Textbausteine. Die Kategorie ist allerdings nicht immer korrekt.
        - !!! Fasse keine Texte zusammen und LASSE AUF KEINEN FALL TEXTE/TEXTBAUSTEINE WEG. Auch wenn Seiten manchmal sehr lang sein können, gib immer die volle ganze Seite aus.
        - Benutze Markdown. Gebe aber keine Codeblock zeichen wie "```markdown" aus.

        Es folgen die durch OCR extrahierten Textbausteine der Seite, welche du verarbeiten sollst:

        <Textbausteine>
        {text_elements_yaml}
        </Textbausteine>

        Im Anhang findest du die Dokumentseite auch einmal als Bild, damit du das Layout noch besser verstehst.
        """
        self.prompt_template = PromptTemplate.from_template(self.prompt_template_string)
        self.open_ai_client = OpenAI()

    def reconstruct_file(self, file: File, temp_file_dir_path: str):
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Started reconstructing"
        )
        pages_dir_path = os.path.join(temp_file_dir_path, "pages")
        text_pages = []
        page_dir_names = sorted(os.listdir(pages_dir_path))
        filtered_page_dir_names = []
        for page_dir_name in page_dir_names:
            if page_dir_name == ".DS_Store":
                continue
            filtered_page_dir_names.append(page_dir_name)
        for page_dir_name in filtered_page_dir_names:
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_dir_name}: Started reconstructing page"
            )
            page_dir_path = os.path.join(pages_dir_path, page_dir_name)
            text_elements_yaml_file_path = os.path.join(
                page_dir_path, "text_elements.yaml"
            )
            with open(text_elements_yaml_file_path, "r") as yaml_file:
                text_elements_yaml = yaml_file.read()
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_dir_name}: Started converting page to JPEG"
            )
            page_pdf_file_path = os.path.join(page_dir_path, "page.pdf")
            page_images = pdf2image.convert_from_path(page_pdf_file_path, dpi=75)
            page_jpeg_file_path = os.path.join(page_dir_path, "page.jpeg")
            page_images[0].save(page_jpeg_file_path, "JPEG")
            with open(page_jpeg_file_path, "rb") as page_jpeg_file:
                page_jpeg_file_content = page_jpeg_file.read()
            file_jpeg_file_content_base64 = base64.b64encode(
                page_jpeg_file_content
            ).decode("utf-8")
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_dir_name}: Finished converting page to JPEG"
            )
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_dir_name}: Started calling LLM"
            )
            response = self.open_ai_client.chat.completions.create(
                model="gpt-4o",
                temperature=0,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.prompt_template.format(
                                    text_elements_yaml=text_elements_yaml
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{file_jpeg_file_content_base64}",
                                },
                            },
                        ],
                    }
                ],
            )
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_dir_name}: Finished calling LLM"
            )
            open_ai_response_text = response.choices[0].message.content
            text_md_file_path = os.path.join(page_dir_path, "text.md")
            with open(text_md_file_path, "w") as text_md_file:
                text_md_file.write(open_ai_response_text)
            text_pages.append(open_ai_response_text)
            logging.info(
                f"{self.__class__.__name__}: File: {file.id}: Page {page_dir_name}: Finished reconstructing page"
            )
        text_md_file_path = os.path.join(temp_file_dir_path, "text.md")
        with open(text_md_file_path, "w") as text_md_file:
            text_md_file.write("\n\n".join(text_pages))
        text_lines_md_file_path = os.path.join(temp_file_dir_path, "text_lines.md")
        with open(text_lines_md_file_path, "w") as text_lines_md_file:
            with open(text_md_file_path, "r") as text_md_file:
                for line_number, line in enumerate(text_md_file, start=1):
                    text_lines_md_file.write(f"{line_number}: {line}")
        logging.info(
            f"{self.__class__.__name__}: File: {file.id}: Finished reconstructing"
        )
