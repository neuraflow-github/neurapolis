from retriever.services.db_session_builder import db_session_builder
from retriever.state.file_section_state import FileSectionState
from retriever.state.hit_state import HitState
from retriever.state.hit_step import HitStep
from retriever.state.search_step import SearchStep
from retriever.state.state import State


def cleaner_node(state: State):
    # Mark hits as doubled when they have the same file section as other hits
    unique_hits: list[HitState] = []
    for x_search in state.searches:
        for x_hit in x_search.hits:
            existing_unique_hit = None
            for y_unique_hit in unique_hits:
                if (
                    y_unique_hit.file_chunk.file_section_id
                    == x_hit.file_chunk.file_section_id
                ):
                    existing_unique_hit = y_unique_hit
                    break
            if existing_unique_hit:
                x_hit.step = HitStep.DOUBLED
                x_hit.doubled_hit = existing_unique_hit
            else:
                x_hit.step = HitStep.NOT_DOUBLED
                unique_hits.append(x_hit)

    # Retrieve the file sections of the hits (Parent document retrieval)
    # Find out which file sections need to get downloaded
    unique_required_file_section_ids: list[str] = []
    for x_search in state.searches:
        for x_hit in x_search.hits:
            if (
                x_hit.step != HitStep.NOT_DOUBLED
                or x_hit.file_chunk.file_section_id in unique_required_file_section_ids
            ):
                continue
            unique_required_file_section_ids.append(x_hit.file_chunk.file_section_id)

    # Download the file sections
    with db_session_builder.build() as db_session:
        file_section_db_results = db_session.run(
            """
            MATCH (file_node:File)-[:FILE_HAS_FILE_SECTION]->(file_section_node:FileSection)
            WHERE file_section_node.id IN $file_section_ids
            RETURN file_section_node, file_node.id AS file_id
            """,
            file_section_ids=unique_required_file_section_ids,
        )
        file_sections: list[FileSectionState] = []
        for file_section_db_result in file_section_db_results:
            file_sections.append(
                FileSectionState.from_db_dict(
                    file_section_db_result["file_section_node"],
                    file_section_db_result["file_id"],
                )
            )

    # Assign the file sections to the hits
    for x_search in state.searches:
        for x_hit in x_search.hits:
            if x_hit.step != HitStep.NOT_DOUBLED:
                continue
            for x_file_section in file_sections:
                if x_hit.file_chunk.file_section_id != x_file_section.id:
                    continue
                x_hit.file_section = x_file_section
                x_hit.step = HitStep.FILE_SECTION_RETRIEVED
                break
        x_search.step = SearchStep.CLEANED

    for x_search in state.searches:
        for x_hit in x_search.hits:
            print(x_hit.file_section is None)

    return {"searches": state.searches}
