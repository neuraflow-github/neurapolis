from typing import Optional, Any, Dict
import uuid
import copy
from dotenv import load_dotenv
import asyncio
import nest_asyncio
from langchain_core.messages import HumanMessage

load_dotenv()

import os
import sys

# # Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from src.agent import graph

# Apply nest_asyncio to allow running asyncio in Jupyter
nest_asyncio.apply()

assistant_id = "pPUGvnnPWZLGtjVFMhSt"

# Generate a unique thread ID for the entire conversation
thread_id = str(uuid.uuid4())
print(thread_id)
config = {
    "configurable": {
        "thread_id": f"{assistant_id}_{thread_id}",
        "model_name": "openai",
        "search_kwargs": {
            "namespace": f"{assistant_id}_DEVELOPMENT",
            "k": 5,
        },
        "language_code": "en-GB",
    }
}
messages = []


async def process_user_input(user_input):
    messages.append(user_input)
    # graph = await create_graph()

    state = {"messages": messages}

    async for event in graph.astream_events(state, config, version="v1"):
        kind = event["event"]

        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if isinstance(chunk.content, list):
                for item in chunk.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        print(item["text"], end="", flush=True)
            else:
                print(chunk.content, end="", flush=True)
        elif kind == "on_tool_start":
            print("\n--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--\n")


async def main():
    try:

        while True:
            user_input = input("\nEnter your question (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break
            await process_user_input(HumanMessage(content=user_input))
    except RuntimeError as e:
        print(f"An error occurred: {e}")
        print(
            "Please ensure the AsyncConnectionPool is properly initialized in the agent.py file."
        )


if __name__ == "__main__":
    asyncio.run(main())
