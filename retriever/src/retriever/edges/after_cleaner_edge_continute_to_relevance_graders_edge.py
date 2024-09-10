from langgraph.constants import Send

from retriever.state.search_step import SearchStep
from retriever.state.state import State


def after_cleaner_edge_continute_to_relevance_graders_edge(state: State) -> list[Send]:
    sends = []
    for x_search in state.searches:
        if x_search.step != SearchStep.CLEANED:
            continue
        sends.append(Send("relevance_grader", x_search))
    return sends
