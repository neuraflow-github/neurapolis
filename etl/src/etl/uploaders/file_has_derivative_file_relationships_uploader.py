from typing import Dict, List

from etl.loaders.files_loader import FilesLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class FileHasDerivativeFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "File",
            "File",
            "FILE_HAS_DERIVATIVE_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        files = FilesLoader().load_saved_items()
        pairs = []
        for x_file in files:
            if x_file.derivative_file is None:
                continue
            for y_derivative_file_id in x_file.derivative_file:
                pair = {
                    "start_id": x_file.id,
                    "end_id": y_derivative_file_id,
                }
                pairs.append(pair)
        return pairs
