from typing import List

from etl.models.location import Location

from .bodies_loader import BodiesLoader
from .extractor_base_loader import ExtractorBaseLoader
from .meetings_loader import MeetingsLoader
from .organizations_loader import OrganizationsLoader
from .papers_loader import PapersLoader


class LocationsLoader(ExtractorBaseLoader[Location]):
    def __init__(self):
        super().__init__(Location, "location", "locations")

    def _extract_items(self) -> List[Location]:
        body = BodiesLoader().load_saved_items()[0]
        organizations = OrganizationsLoader().load_saved_items()
        meetings = MeetingsLoader().load_saved_items()
        papers = PapersLoader().load_saved_items()
        locations = []
        if body.location:
            locations.append(body.location)
        for x_organization in organizations:
            if x_organization.location is None:
                continue
            locations.append(x_organization.location)
        for x_meeting in meetings:
            if x_meeting.location is None:
                continue
            locations.append(x_meeting.location)
        for x_paper in papers:
            if x_paper.location is None:
                continue
            locations.extend(x_paper.location)
        return locations
