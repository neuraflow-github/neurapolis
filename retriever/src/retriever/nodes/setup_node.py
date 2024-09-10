from langchain_core.runnables.config import RunnableConfig

from retriever.state.state import State


def setup_node(state: State, config: RunnableConfig):
    if state.query == "":
        raise Exception("Query is empty")
    if config["configurable"].get("search_count") is None:
        config["configurable"]["search_count"] = 3
    if config["configurable"].get("search_top_k") is None:
        config["configurable"]["search_top_k"] = 10
    return state
