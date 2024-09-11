from datetime import datetime
from typing import Dict, List, Optional

from .consultation import Consultation
from .db_dict import DbDict
from .file import File
from .location import Location
from .ris_api_dto import RisApiDto


class Paper(RisApiDto, DbDict):
    id: Optional[str]
    type: Optional[str]
    body: Optional[str]
    name: Optional[str]
    reference: Optional[str]
    date: Optional[str]
    paper_type: Optional[str]
    related_paper: Optional[List[str]]
    superordinated_paper: Optional[List[str]]
    subordinated_paper: Optional[List[str]]
    main_file: Optional[File]
    auxiliary_file: Optional[List[File]]
    location: Optional[List[Location]]
    originator_person: Optional[List[str]]
    under_direction_of: Optional[List[str]]
    originator_organization: Optional[List[str]]
    consultation: Optional[List[Consultation]]
    license: Optional[str]
    keyword: Optional[List[str]]
    created: Optional[datetime]
    modified: Optional[datetime]
    web: Optional[str]
    deleted: Optional[bool]

    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        body: Optional[str],
        name: Optional[str],
        reference: Optional[str],
        date: Optional[str],
        paper_type: Optional[str],
        related_paper: Optional[List[str]],
        superordinated_paper: Optional[List[str]],
        subordinated_paper: Optional[List[str]],
        main_file: Optional[File],
        auxiliary_file: Optional[List[File]],
        location: Optional[List[Location]],
        originator_person: Optional[List[str]],
        under_direction_of: Optional[List[str]],
        originator_organization: Optional[List[str]],
        consultation: Optional[List[Consultation]],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.body = body
        self.name = name
        self.reference = reference
        self.date = date
        self.paper_type = paper_type
        self.related_paper = related_paper
        self.superordinated_paper = superordinated_paper
        self.subordinated_paper = subordinated_paper
        self.main_file = main_file
        self.auxiliary_file = auxiliary_file
        self.location = location
        self.originator_person = originator_person
        self.under_direction_of = under_direction_of
        self.originator_organization = originator_organization
        self.consultation = consultation
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(paper_ris_api_dto: Dict) -> "Paper":
        return Paper(
            id=paper_ris_api_dto.get("id"),
            type=paper_ris_api_dto.get("type"),
            body=paper_ris_api_dto.get("body"),
            name=paper_ris_api_dto.get("name"),
            reference=paper_ris_api_dto.get("reference"),
            date=paper_ris_api_dto.get("date"),
            paper_type=paper_ris_api_dto.get("paperType"),
            related_paper=paper_ris_api_dto.get("relatedPaper"),
            superordinated_paper=paper_ris_api_dto.get("superordinatedPaper"),
            subordinated_paper=paper_ris_api_dto.get("subordinatedPaper"),
            main_file=(
                File.from_ris_api_dto(paper_ris_api_dto.get("mainFile"))
                if paper_ris_api_dto.get("mainFile")
                else None
            ),
            auxiliary_file=(
                [
                    File.from_ris_api_dto(x_file_ris_api_dto)
                    for x_file_ris_api_dto in paper_ris_api_dto.get("auxiliaryFile")
                ]
                if paper_ris_api_dto.get("auxiliaryFile")
                else None
            ),
            location=(
                [
                    Location.from_ris_api_dto(x_location_ris_api_dto)
                    for x_location_ris_api_dto in paper_ris_api_dto.get("location")
                ]
                if paper_ris_api_dto.get("location")
                else None
            ),
            originator_person=paper_ris_api_dto.get("originatorPerson"),
            under_direction_of=paper_ris_api_dto.get("underDirectionOf"),
            originator_organization=paper_ris_api_dto.get("originatorOrganization"),
            consultation=(
                [
                    Consultation.from_ris_api_dto(x_consultation_ris_api_dto)
                    for x_consultation_ris_api_dto in paper_ris_api_dto.get(
                        "consultation", []
                    )
                ]
                if paper_ris_api_dto.get("consultation")
                else None
            ),
            license=paper_ris_api_dto.get("license"),
            keyword=paper_ris_api_dto.get("keyword"),
            created=paper_ris_api_dto.get("created"),
            modified=paper_ris_api_dto.get("modified"),
            web=paper_ris_api_dto.get("web"),
            deleted=paper_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "body": self.body,
            "name": self.name,
            "reference": self.reference,
            "date": self.date,
            "paper_type": self.paper_type,
            "related_paper": self.related_paper,
            "superordinated_paper": self.superordinated_paper,
            "subordinated_paper": self.subordinated_paper,
            "main_file": self.main_file.to_dict() if self.main_file else None,
            "auxiliary_file": (
                [file.to_dict() for file in self.auxiliary_file]
                if self.auxiliary_file
                else None
            ),
            "location": (
                [loc.to_dict() for loc in self.location] if self.location else None
            ),
            "originator_person": self.originator_person,
            "under_direction_of": self.under_direction_of,
            "originator_organization": self.originator_organization,
            "consultation": (
                [cons.to_dict() for cons in self.consultation]
                if self.consultation
                else None
            ),
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def to_db_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            # "body": self.body,
            "name": self.name,
            "reference": self.reference,
            "date": self.date,
            "paper_type": self.paper_type,
            # "related_paper": self.related_paper,
            # "superordinated_paper": self.superordinated_paper,
            # "subordinated_paper": self.subordinated_paper,
            # "main_file": self.main_file,
            # "auxiliary_file": self.auxiliary_file,
            # "location": self.location,
            # "originator_person": self.originator_person,
            # "under_direction_of": self.under_direction_of,
            # "originator_organization": self.originator_organization,
            # "consultation": self.consultation,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
