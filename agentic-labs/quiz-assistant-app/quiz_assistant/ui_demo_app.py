"""The presentation layer for the streamlit app"""

import streamlit as st  # all streamlit commands will be available through the "st" alias
from quiz_assistant import ui_demo_logic  # reference to local logic script


st.set_page_config(page_title="Quiz Assistant", layout="wide")  # HTML title
st.title("Quiz Assistant")  # page title

if "chat_history" not in st.session_state:  # see if the chat history hasn't been created yet
    st.session_state.chat_history = []  # initialize the chat history


chat_column, quiz_column = st.columns(2)

with chat_column:
    chat_container = st.container(height=500)

with quiz_column:
    quiz_container = st.container(height=500)

# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:  # loop through the chat history
    # renders a chat line for the given role, containing everything in the with block
    with chat_container.chat_message(message.role):
        st.markdown(message.text)  # display the chat content


input_text = st.chat_input("Chat with your bot here")  # display a chat input box

if input_text:
    with chat_container.chat_message("user"):
        st.markdown(input_text)

    with st.spinner("Thinking...."):
        response = ui_demo_logic.chat_with_agent(message_history=st.session_state.chat_history, new_text=input_text)

        with chat_container.chat_message("assistant"):  # display user message in chat message container
            st.markdown(response)

        for tool_result in response.state.get("tool_results", []):

            if tool_result["status"] == "success":
                if tool_result.get("content"):
                    quiz_content = tool_result.get("content")[0].get("json", None)
                    if quiz_content:
                        st.session_state.quiz = quiz_content


with quiz_container:
    if "quiz" in st.session_state:
        quiz = st.session_state.quiz
        st.header(quiz["quiz_title"])

        # BEGIN CHALLENGE CONTENT: Present the quiz content (change if you came up with your own structure) -----

        for q in quiz["questions"]:
            st.markdown(f"**{q["question_text"]}**")

            for c in q["choices"]:
                answer_indicator = " (correct)" if c["is_correct_answer"] else ""

                st.markdown(f"{c["choice_label"]}) {c["choice_text"]}{answer_indicator}")

            with st.expander("Explanation"):
                st.write(q["explanation"])

        # END CHALLENGE CONTENT --------------------------------------------------------------------------------

        download_button = st.download_button("Download", data=ui_demo_logic.create_download_content(quiz))
