from typing import List

from etl.models.consultation import Consultation

from .extractor_base_loader import ExtractorBaseLoader
from .papers_loader import PapersLoader


class ConsultationsLoader(ExtractorBaseLoader[Consultation]):
    def __init__(self):
        super().__init__(Consultation, "consultation", "consultations")

    def _extract_items(self) -> List[Consultation]:
        papers = PapersLoader().load_saved_items()
        consultations = []
        for x_paper in papers:
            if not x_paper.consultation:
                continue
            for y_consultation in x_paper.consultation:
                is_existing = False
                for z_existing_consultation in consultations:
                    if y_consultation.id == z_existing_consultation.id:
                        is_existing = True
                        break
                if is_existing:
                    continue
                consultations.append(y_consultation)
        return consultations
