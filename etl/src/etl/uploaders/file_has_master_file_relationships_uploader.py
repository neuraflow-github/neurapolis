from typing import Dict, List

from etl.loaders.files_loader import FilesLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class FileHasMasterFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "File",
            "File",
            "FILE_HAS_MASTER_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        files = FilesLoader().load_saved_items()
        pairs = []
        for x_file in files:
            if x_file.master_file is None:
                continue
            pair = {"start_id": x_file.id, "end_id": x_file.master_file}
            pairs.append(pair)
        return pairs


if __name__ == "__main__":
    FileHasMasterFileRelationshipsUploader().upload_items()
