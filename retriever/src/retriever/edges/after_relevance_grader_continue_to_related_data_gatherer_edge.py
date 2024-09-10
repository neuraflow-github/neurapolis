from langgraph.constants import Send

from retriever.state.search_step import SearchStep
from retriever.state.state import State


def after_relevance_grader_continue_to_related_data_gatherer_edge(state: State):
    sends = []
    for x_search in state.searches:
        if (
            x_search.state != SearchStep.RELEVANCE_GRADED
            or not x_search.grading.is_relevant
        ):
            continue
        sends.append(Send("related_data_gatherer", x_search))
    return sends
