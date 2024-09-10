from langgraph.constants import Send

from retriever.state.search_step import SearchStep
from retriever.state.state import State


def after_planner_continue_to_retrievers_edge(state: State) -> list[Send]:
    sends = []
    for x_search in state.searches:
        if x_search.step != SearchStep.PLANNED:
            continue
        sends.append(Send("retriever", x_search))
    return sends
