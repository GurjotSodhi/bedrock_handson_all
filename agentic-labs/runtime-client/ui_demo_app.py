"""The presentation layer for the streamlit app"""

import uuid
import streamlit as st  # all streamlit commands will be available through the "st" alias
import ui_demo_logic  # reference to local logic script

st.set_page_config(page_title="Chatbot using AgentCore")  # HTML title
st.title("Chatbot using AgentCore")  # page title


if "chat_history" not in st.session_state:  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history
    st.session_state.session_id = str(uuid.uuid4())

st.subheader(f"Session: {st.session_state.session_id}")

chat_container = st.container()

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
        response = ui_demo_logic.chat_with_agent(
            message_history=st.session_state.chat_history,
            session_id=st.session_state.session_id,
            new_text=input_text
        )

        with chat_container.chat_message("assistant"):
            st.markdown(response)
