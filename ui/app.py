from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tracers import LangChainTracer
from langchain_core.tracers.run_collector import RunCollectorCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langsmith import Client
import streamlit as st
from streamlit_feedback import streamlit_feedback
import time
import uuid
from langserve import RemoteRunnable
from langchain import callbacks

import os
from dotenv import load_dotenv

load_dotenv()

# Import secrets from environment variables

LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")
LANGCHAIN_ENDPOINT = os.environ.get("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.environ.get("LANGCHAIN_PROJECT")
CHAIN_URL = os.environ.get("CHAIN_URL")

st.set_page_config(page_title="Ratsinformationssystem", page_icon="🏛️")
st.title("Ratsinformationssystem")


langchain_api_key = LANGCHAIN_API_KEY
project = LANGCHAIN_PROJECT


langchain_endpoint = "https://eu.api.smith.langchain.com"
client = Client(api_url=langchain_endpoint, api_key=langchain_api_key)
ls_tracer = LangChainTracer(project_name=project, client=client)
run_collector = RunCollectorCallbackHandler()

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

cfg = RunnableConfig(
    {
        "configurable": {
            "session_id": st.session_state["session_id"],
            "thread_id": st.session_state["thread_id"],
        }
    }
)
cfg["callbacks"] = [ls_tracer, run_collector]

msgs = StreamlitChatMessageHistory(key="langchain_messages")

reset_history = st.button("Neue Anfrage starten")
if len(msgs.messages) == 0 or reset_history:
    msgs.clear()
    msgs.add_messages(
        [
            AIMessage(
                content="Willkommen beim Ratsinformationssystem! Wie kann ich Ihnen bei Ihrer Suche nach Informationen über städtische Verwaltungsaktivitäten, Entscheidungen oder damit verbundene Einrichtungen helfen?"
            )
        ]
    )
    st.session_state["last_run"] = None
    st.session_state["thread_id"] = str(
        uuid.uuid4()
    )  # Generate new thread_id for new conversation

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    if isinstance(msg, (HumanMessage, AIMessage)):
        st.chat_message(avatars[msg.type]).write(msg.content)

chain = RemoteRunnable(CHAIN_URL)

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="messages",
    history_messages_key="langchain_messages",
)

if input := st.chat_input(
    placeholder="z.B. 'Welche Beschlüsse wurden zur Stadtentwicklung in den letzten 5 Jahren gefasst?'"
):
    st.chat_message("user").write(input)
    with st.chat_message("assistant"):
        with callbacks.collect_runs() as cb:
            response = chain_with_history.invoke(
                {
                    "messages": [HumanMessage(content=input)],
                },
                cfg,
            )
            st.write(response)
        if cb.traced_runs:
            st.session_state["last_run"] = cb.traced_runs[0].id


@st.cache_data(ttl="2h", show_spinner=False)
def get_run_url(run_id):
    time.sleep(1)
    return client.read_run(run_id).url


if st.session_state.get("last_run"):
    run_url = get_run_url(st.session_state.last_run)

    feedback = streamlit_feedback(
        feedback_type="faces",
        optional_text_label="[Optional] Bitte erläutern Sie Ihre Bewertung:",
        key=f"feedback_{st.session_state.last_run}",
    )

    if feedback:
        scores = {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0}
        client.create_feedback(
            st.session_state.last_run,
            feedback["type"],
            score=scores[feedback["score"]],
            comment=feedback.get("text", None),
        )
        st.toast("Vielen Dank für Ihr Feedback zur Informationsqualität!", icon="📊")
