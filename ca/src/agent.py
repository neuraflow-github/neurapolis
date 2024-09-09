from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END
from src.utils.nodes import call_model, should_continue
from src.utils.state import AgentState


# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai"]


# Define a new graph
workflow = StateGraph(AgentState, config_schema=GraphConfig)


# Define the function to execute tools
async def call_tool(state, config):
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]
    print("Tool Call:", tool_call)

    # from src.utils.tools import Retriever

    # retriever = Retriever()

    query = tool_call["args"]["full_query"]

    # from neo4j_cypher.chain import chain

    docs = []

    # docs = get_relevant_documents(query, config)

    # docs = [doc.dict() for doc in docs]

    import json
    from langchain_core.messages import ToolMessage

    function_message = ToolMessage(
        content=json.dumps(docs), name=tool_call["name"], tool_call_id=tool_call["id"]
    )

    return {"messages": [function_message]}


# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")


from langgraph.checkpoint.memory import MemorySaver

graph = workflow.compile(checkpointer=MemorySaver())
