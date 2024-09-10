from langgraph.graph import END, StateGraph

from retriever.edges.after_cleaner_edge_continute_to_relevance_graders_edge import (
    after_cleaner_edge_continute_to_relevance_graders_edge,
)
from retriever.edges.after_planner_continue_to_retrievers_edge import (
    after_planner_continue_to_retrievers_edge,
)
from retriever.edges.after_relevance_grader_continue_to_related_data_gatherer_edge import (
    after_relevance_grader_continue_to_related_data_gatherer_edge,
)
from retriever.graph_configurable import GraphConfigurable
from retriever.nodes.cleaner_node import cleaner_node
from retriever.nodes.planner_node import planner_node
from retriever.nodes.related_data_gatherer_node import related_data_gatherer_node
from retriever.nodes.relevance_grader_node import relevance_grader_node
from retriever.nodes.retriever_node import retriever_node
from retriever.nodes.setup_node import setup_node
from retriever.state.state import State

graph_builder = StateGraph(State, config_schema=GraphConfigurable)

graph_builder.add_node("setup", setup_node)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("retriever", retriever_node)
graph_builder.add_node("cleaner", cleaner_node)
graph_builder.add_node("relevance_grader", relevance_grader_node)
graph_builder.add_node("related_data_gatherer", related_data_gatherer_node)

graph_builder.set_entry_point("setup")
graph_builder.add_edge("setup", "planner")
graph_builder.add_conditional_edges(
    "planner", after_planner_continue_to_retrievers_edge, ["retriever"]
)
graph_builder.add_edge("retriever", "cleaner")
graph_builder.add_conditional_edges(
    "cleaner",
    after_cleaner_edge_continute_to_relevance_graders_edge,
    ["relevance_grader"],
)
graph_builder.add_conditional_edges(
    "relevance_grader",
    after_relevance_grader_continue_to_related_data_gatherer_edge,
    ["related_data_gatherer"],
)
graph_builder.add_edge("related_data_gatherer", END)

graph = graph_builder.compile()
