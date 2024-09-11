from retriever.state.search_state import SearchState


def related_data_gatherer_node(search_state: SearchState):
    return {"searches": [search_state]}
