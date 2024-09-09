from typing import List

from etl.loaders.files_loader import FilesLoader
from etl.models.file import File

from .nodes_base_uploader import NodesBaseUploader


class FilesUploader(NodesBaseUploader[File]):
    def __init__(self):
        super().__init__(File, "File")

    def _load_items(self) -> List[File]:
        return FilesLoader().load_saved_items()
