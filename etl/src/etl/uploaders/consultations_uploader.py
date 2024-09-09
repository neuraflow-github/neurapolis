from typing import List

from etl.loaders.consultations_loader import ConsultationsLoader
from etl.models.consultation import Consultation

from .nodes_base_uploader import NodesBaseUploader


class ConsultationsUploader(NodesBaseUploader[Consultation]):
    def __init__(self):
        super().__init__(Consultation, "Consultation")

    def _load_items(self) -> List[Consultation]:
        return ConsultationsLoader().load_saved_items()
