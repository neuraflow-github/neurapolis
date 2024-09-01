from typing import List

from etl.loaders.persons_loader import PersonsLoader
from etl.models.person import Person

from .nodes_base_uploader import NodesBaseUploader


class PersonsUploader(NodesBaseUploader[Person]):
    def __init__(self):
        super().__init__(Person, "Person")

    def _load_items(self) -> List[Person]:
        return PersonsLoader().load_saved_items()
