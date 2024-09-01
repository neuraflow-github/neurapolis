from typing import List

from etl.loaders.locations_loader import LocationsLoader
from etl.models.location import Location

from .nodes_base_uploader import NodesBaseUploader


class LocationsUploader(NodesBaseUploader[Location]):
    def __init__(self):
        super().__init__(Location, "Location")

    def _load_items(self) -> List[Location]:
        return LocationsLoader().load_saved_items()
