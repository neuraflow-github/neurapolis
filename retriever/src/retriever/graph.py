from typing import TypedDict

from langgraph.graph import END, StateGraph

from retriever.nodes.search_planner_node import search_planner_node
from retriever.state.state import State


class GraphConfig(TypedDict):
    search_count: int = 3


graph_builder = StateGraph(State, config_schema=GraphConfig)

graph_builder.add_node("search_planner_node", search_planner_node)
graph_builder.add_edge("search_planner_node", END)

graph_builder.set_entry_point("search_planner_node")

graph = graph_builder.compile()
