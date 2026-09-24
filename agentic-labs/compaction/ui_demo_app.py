"""The presentation layer for the streamlit app"""

import streamlit as st  # all streamlit commands will be available through the "st" alias
import ui_demo_logic  # reference to local logic script

st.set_page_config(page_title="Compaction Chatbot", layout="wide")  # HTML title
st.title("Compaction Chatbot")  # page title

if "chat_history" not in st.session_state:  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history

internals_column, chat_column = st.columns(2)

with chat_column:
    chat_container = st.container(height=500)

with internals_column:
    internals_container = st.container()

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
        response, summarization_state, agent_messages = ui_demo_logic.chat_with_agent(
            message_history=st.session_state.chat_history, new_text=input_text
        )

        with chat_container.chat_message("assistant"):  # display user message in chat message container
            st.markdown(response)

        with internals_container:
            st.markdown("**Summary**:")
            summary_message = summarization_state.get("summary_message")
            if summary_message:
                st.write(summary_message["content"][0]["text"])

            st.markdown(f"**Removed messages count:** {summarization_state["removed_message_count"]}")

            st.markdown(f"**Current messages count:** {len(agent_messages)}")

            with st.expander("Current messages of the agent:"):
                st.json(agent_messages)
