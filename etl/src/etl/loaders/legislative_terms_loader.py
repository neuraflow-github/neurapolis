from typing import List

from etl.models.legislative_term import LegislativeTerm

from .base_loader import BaseLoader
from .bodies_loader import BodiesLoader


class LegislativeTermsLoader(BaseLoader[LegislativeTerm]):
    def __init__(self):
        super().__init__(LegislativeTerm, "legislative_term", "legislative_terms")

    def _load_items(
        self, existing_items: List[LegislativeTerm]
    ) -> List[LegislativeTerm]:
        body = BodiesLoader().load_saved_items()[0]
        return body.legislative_term
