"""The presentation layer for the streamlit app"""

import uuid

import streamlit as st  # all streamlit commands will be available through the "st" alias
import ui_demo_logic  # reference to local logic script


st.set_page_config(page_title="Chatbot with Memory", layout="wide")  # HTML title


if "session_id" not in st.query_params:

    st.header("Resume session:")

    sessions = ui_demo_logic.get_sessions()

    for session in sessions:
        session_created = session["createdAt"].strftime("%Y-%m-%d %H:%M:%S")
        session_label = f"Conversation with {session['actorId']} started {session_created}"
        sid = session["sessionId"]
        st.link_button(label=session_label, url=f"?session_id={sid}")

    st.link_button(label="Start New Session", url="?session_id=new")

    st.stop()
elif st.query_params["session_id"] == "new":
    session_id = str(uuid.uuid4())
else:
    session_id = st.query_params["session_id"]

if "chat_history" not in st.session_state:  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history

    # Create ChatSession instance and store it in session state
    st.session_state.chat_session = ui_demo_logic.ChatSession(
        session_id=session_id, message_history=st.session_state.chat_history
    )


st.title(f"Chatbot: {st.session_state.chat_session.session_id}")  # page title


internals_column, chat_column = st.columns(2)

with chat_column:
    chat_container = st.container(height=500)

with internals_column:
    st.header("Memory")

    st.subheader("Retrieved memory passed to model")

    retrieved_memory_placeholder = st.container()

    st.subheader("Long-term memory records")
    refresh_memory_button = st.button("Display memories")

    if refresh_memory_button:
        prefix_dicts = st.session_state.chat_session.get_memories()

        for prefix_dict in prefix_dicts:
            st.subheader(prefix_dict["prefix"])

            st.write(prefix_dict["memories"])


# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:  # loop through the chat history
    # renders a chat line for the given role, containing everything in the with block
    with chat_container.chat_message(message.role):
        st.markdown(message.text)  # display the chat content


input_text = st.chat_input("Chat with your bot here")  # display a chat input box

if input_text:
    with chat_container.chat_message("user"):
        st.markdown(input_text)  # Display user's posted message

    with st.spinner("Thinking...."):
        response, memory_retrieval_text = st.session_state.chat_session.chat(new_text=input_text)

        with chat_container.chat_message("assistant"):
            st.markdown(response)

        retrieved_memory_placeholder.write(memory_retrieval_text)
