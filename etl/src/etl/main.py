import os
import sys

from etl.loaders.agenda_items_loader import AgendaItemsLoader
from etl.loaders.base_loader import BaseLoader
from etl.loaders.bodies_loader import BodiesLoader
from etl.loaders.consultations_loader import ConsultationsLoader
from etl.loaders.files_loader import FilesLoader
from etl.loaders.legislative_terms_loader import LegislativeTermsLoader
from etl.loaders.locations_loader import LocationsLoader
from etl.loaders.meetings_loader import MeetingsLoader
from etl.loaders.memberships_loader import MembershipsLoader
from etl.loaders.organizations_loader import OrganizationsLoader
from etl.loaders.papers_loader import PapersLoader
from etl.loaders.persons_loader import PersonsLoader
from etl.transformers.files_transformer.files_transformer import FilesTransformer
from etl.uploaders.agenda_item_has_auxiliary_file_relationships_uploader import (
    AgendaItemHasAuxiliaryFileRelationshipsUploader,
)
from etl.uploaders.agenda_item_has_consultation_relationships_uploader import (
    AgendaItemHasConsultationRelationshipsUploader,
)
from etl.uploaders.agenda_item_has_resolution_file_relationships_uploader import (
    AgendaItemHasResolutionFileRelationshipsUploader,
)
from etl.uploaders.agenda_items_uploader import AgendaItemsUploader
from etl.uploaders.base_uploader import BaseUploader
from etl.uploaders.body_has_legislative_term_relationships_uploader import (
    BodyHasLegislativeTermRelationshipsUploader,
)
from etl.uploaders.body_has_location_relationships_uploader import (
    BodyHasLocationRelationshipsUploader,
)
from etl.uploaders.body_has_meeting_relationships_uploader import (
    BodyHasMeetingRelationshipsUploader,
)
from etl.uploaders.body_has_organization_relationships_uploader import (
    BodyHasOrganizationRelationshipsUploader,
)
from etl.uploaders.body_has_paper_relationships_uploader import (
    BodyHasPaperRelationshipsUploader,
)
from etl.uploaders.body_has_person_relationships_uploader import (
    BodyHasPersonRelationshipsUploader,
)
from etl.uploaders.body_uploader import BodyUploader
from etl.uploaders.consultation_has_meeting_relationships_uploader import (
    ConsultationHasMeetingRelationshipsUploader,
)
from etl.uploaders.consultations_uploader import ConsultationsUploader
from etl.uploaders.file_has_derivative_file_relationships_uploader import (
    FileHasDerivativeFileRelationshipsUploader,
)
from etl.uploaders.file_has_master_file_relationships_uploader import (
    FileHasMasterFileRelationshipsUploader,
)
from etl.uploaders.files_uploader import FilesUploader
from etl.uploaders.legislative_terms_uploader import LegislativeTermsUploader
from etl.uploaders.locations_uploader import LocationsUploader
from etl.uploaders.meeting_has_agenda_item_relationships_uploader import (
    MeetingHasAgendaItemRelationshipsUploader,
)
from etl.uploaders.meeting_has_auxiliary_file_relationships_uploader import (
    MeetingHasAuxiliaryFileRelationshipsUploader,
)
from etl.uploaders.meeting_has_invitation_file_relationships_uploader import (
    MeetingHasInvitationFileRelationshipsUploader,
)
from etl.uploaders.meeting_has_location_relationships_uploader import (
    MeetingHasLocationRelationshipsUploader,
)
from etl.uploaders.meeting_has_results_protocol_file_relationships_uploader import (
    MeetingHasResultsProtocolFileRelationshipsUploader,
)
from etl.uploaders.meeting_has_verbatim_protocol_file_relationships_uploader import (
    MeetingHasVerbatimProtocolFileRelationshipsUploader,
)
from etl.uploaders.meetings_uploader import MeetingsUploader
from etl.uploaders.membership_has_on_behalf_of_relationships_uploader import (
    MembershipHasOnBehalfOfRelationshipsUploader,
)
from etl.uploaders.memberships_uploader import MembershipsUploader
from etl.uploaders.organization_has_consultation_relationships_uploader import (
    OrganizationHasConsultationRelationshipsUploader,
)
from etl.uploaders.organization_has_location_relationships_uploader import (
    OrganizationHasLocationRelationshipsUploader,
)
from etl.uploaders.organization_has_meeting_relationships_uploader import (
    OrganizationHasMeetingRelationshipsUploader,
)
from etl.uploaders.organization_has_membership_relationships_uploader import (
    OrganizationHasMembershipRelationshipsUploader,
)
from etl.uploaders.organization_has_sub_organization_relationships_uploader import (
    OrganizationHasSubOrganizationRelationshipsUploader,
)
from etl.uploaders.organizations_uploader import OrganizationsUploader
from etl.uploaders.paper_has_auxiliary_file_relationships_uploader import (
    PaperHasAuxiliaryFileRelationshipsUploader,
)
from etl.uploaders.paper_has_consultation_relationships_uploader import (
    PaperHasConsultationRelationshipsUploader,
)
from etl.uploaders.paper_has_location_relationships_uploader import (
    PaperHasLocationRelationshipsUploader,
)
from etl.uploaders.paper_has_main_file_relationships_uploader import (
    PaperHasMainFileRelationshipsUploader,
)
from etl.uploaders.paper_has_originator_organization_relationships_uploader import (
    PaperHasOriginatorOrganizationRelationshipsUploader,
)
from etl.uploaders.paper_has_originator_person_relationships_uploader import (
    PaperHasOriginatorPersonRelationshipsUploader,
)
from etl.uploaders.paper_has_related_paper_relationships_uploader import (
    PaperHasRelatedPaperRelationshipsUploader,
)
from etl.uploaders.paper_has_subordinated_paper_relationships_uploader import (
    PaperHasSubordinatedPaperRelationshipsUploader,
)
from etl.uploaders.paper_has_superordinated_paper_relationships_uploader import (
    PaperHasSuperordinatedPaperRelationshipsUploader,
)
from etl.uploaders.paper_has_under_direction_of_relationships_uploader import (
    PaperHasUnderDirectionOfRelationshipsUploader,
)
from etl.uploaders.papers_uploader import PapersUploader
from etl.uploaders.person_has_meeting_relationships_uploader import (
    PersonHasMeetingRelationshipsUploader,
)
from etl.uploaders.person_has_membership_relationships_uploader import (
    PersonHasMembershipRelationshipsUploader,
)
from etl.uploaders.persons_uploader import PersonsUploader
from etl.utilities.setup_logging import setup_logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    setup_logging()

    # # Load
    # BodiesLoader().load_and_save_items()
    # loaders: BaseLoader = [
    #     LegislativeTermsLoader(),
    #     OrganizationsLoader(),
    #     PersonsLoader(),
    #     MembershipsLoader(),
    #     MeetingsLoader(),
    #     AgendaItemsLoader(),
    #     PapersLoader(),
    #     ConsultationsLoader(),
    #     FilesLoader(),
    #     LocationsLoader(),
    # ]
    # for x_loader in loaders:
    #     x_loader.load_and_save_items()

    # # Upload
    # uploaders: BaseUploader = [
    #     BodyUploader(),
    #     #
    #     LegislativeTermsUploader(),
    #     BodyHasLegislativeTermRelationshipsUploader(),
    #     #
    #     OrganizationsUploader(),
    #     BodyHasOrganizationRelationshipsUploader(),
    #     OrganizationHasSubOrganizationRelationshipsUploader(),
    #     #
    #     PersonsUploader(),
    #     BodyHasPersonRelationshipsUploader(),
    #     #
    #     MembershipsUploader(),
    #     OrganizationHasMembershipRelationshipsUploader(),
    #     PersonHasMembershipRelationshipsUploader(),
    #     MembershipHasOnBehalfOfRelationshipsUploader(),
    #     #
    #     MeetingsUploader(),
    #     BodyHasMeetingRelationshipsUploader(),
    #     OrganizationHasMeetingRelationshipsUploader(),
    #     PersonHasMeetingRelationshipsUploader(),
    #     #
    #     AgendaItemsUploader(),
    #     MeetingHasAgendaItemRelationshipsUploader(),
    #     #
    #     PapersUploader(),
    #     BodyHasPaperRelationshipsUploader(),
    #     PaperHasRelatedPaperRelationshipsUploader(),
    #     PaperHasSuperordinatedPaperRelationshipsUploader(),
    #     PaperHasSubordinatedPaperRelationshipsUploader(),
    #     PaperHasOriginatorPersonRelationshipsUploader(),
    #     PaperHasUnderDirectionOfRelationshipsUploader(),
    #     PaperHasOriginatorOrganizationRelationshipsUploader(),
    #     #
    #     ConsultationsUploader(),
    #     OrganizationHasConsultationRelationshipsUploader(),
    #     AgendaItemHasConsultationRelationshipsUploader(),
    #     PaperHasConsultationRelationshipsUploader(),
    #     ConsultationHasMeetingRelationshipsUploader(),
    #     #
    #     FilesUploader(),
    #     MeetingHasInvitationFileRelationshipsUploader(),
    #     MeetingHasResultsProtocolFileRelationshipsUploader(),
    #     MeetingHasVerbatimProtocolFileRelationshipsUploader(),
    #     MeetingHasAuxiliaryFileRelationshipsUploader(),
    #     AgendaItemHasResolutionFileRelationshipsUploader(),
    #     AgendaItemHasAuxiliaryFileRelationshipsUploader(),
    #     PaperHasMainFileRelationshipsUploader(),
    #     PaperHasAuxiliaryFileRelationshipsUploader(),
    #     FileHasMasterFileRelationshipsUploader(),
    #     FileHasDerivativeFileRelationshipsUploader(),
    #     #
    #     LocationsUploader(),
    #     BodyHasLocationRelationshipsUploader(),
    #     OrganizationHasLocationRelationshipsUploader(),
    #     MeetingHasLocationRelationshipsUploader(),
    #     PaperHasLocationRelationshipsUploader(),
    # ]
    # for x_uploader in uploaders:
    #     x_uploader.upload_items()

    # Transform
    FilesTransformer().transform_files()
