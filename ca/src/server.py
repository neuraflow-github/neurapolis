from typing import Any, Dict
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
import uuid
import copy
from dotenv import load_dotenv
from src.agent import graph
from langchain_core.runnables import chain
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Union
import logging


load_dotenv()

app = FastAPI()

# Allow all origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Middleware to modify configuration per request
async def middleware(config: Dict[str, Any], req: Request) -> Dict[str, Any]:
    print(f"\033[34mconfig:\033[0m {config}")
    body = await req.json()
    print(f"Request Body: {body}")
    config["configurable"] = body["config"].get(
        "configurable", {"thread_id": str(uuid.uuid4())}
    )
    print(f"\033[34mconfig:\033[0m {config}")
    return config


# Define the graph chain
@chain
async def graph_chain(inputs, config):
    print(f"\033[34mconfig:\033[0m {config}")
    # if config.get("configurable", {}).get("thread_id") is None:
    #     config["configurable"]["thread_id"] = str(uuid.uuid4())
    # print("\033[34mconfigurable:\033[0m", config["configurable"])
    # print("\033[34minputs:\033[0m", inputs)

    # Use the search_kwargs from the config if available, otherwise use default
    # search_kwargs = config.get("configurable", {}).get(
    #     "search_kwargs", {"namespace": "NOLM3uYRuP5yhJNU1JOF_DEVELOPMENT", "k": 5}
    # )
    # config["configurable"]["search_kwargs"] = search_kwargs

    inputs_copy = copy.deepcopy(inputs)
    # Check if 'messages' key exists, if not, fall back to 'undefined'
    messages = inputs_copy.get("messages", inputs_copy.get("undefined", []))
    for message in messages:
        if "type" in message:
            message["role"] = message.pop("type")

    from langchain_core.messages.utils import convert_to_messages

    messages = convert_to_messages(messages)
    state = {"messages": messages}

    async for event in graph.astream_events(state, config, version="v1"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if isinstance(chunk.content, list):
                for item in chunk.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        yield item["text"]
            else:
                content = chunk.content
                print("\033[32m" + content + "\033[0m", flush=True, end=" ")
                yield content
        elif kind == "on_tool_start":
            yield f"\nStarting tool: {event['name']} with inputs: {event['data'].get('input')}\n"
        elif kind == "on_tool_end":
            yield f"\nTool {event['name']} finished. Output: {event['data'].get('output')}\n"


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )


logging.getLogger().setLevel(logging.ERROR)  # hide warning log

add_routes(
    app,
    graph_chain,
    path="/chat",
    enable_feedback_endpoint=True,
    playground_type="chat",
    per_req_config_modifier=middleware,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
