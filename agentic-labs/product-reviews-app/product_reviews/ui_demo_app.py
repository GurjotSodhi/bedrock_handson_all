"""The presentation layer for the streamlit app"""

import streamlit as st
from product_reviews import ui_demo_logic

st.set_page_config(page_title="Review Analyzer", layout="wide")  # HTML title
st.title("Review Analyzer")  # page title

entry_col, results_col = st.columns(2)

with entry_col:

    review_title = st.text_input("Review title")

    review_content = st.text_area("Review content")

    stars_rating = st.feedback(options="stars")

    go_button = st.button("Go", type="primary")  # display a primary button


with results_col:
    if go_button:
        with st.spinner("Thinking...."):
            result = ui_demo_logic.process_content(
                review_title=review_title, review_content=review_content, stars_rating=stars_rating
            )

            st.subheader("Result")

            friendly_tab, json_tab = st.tabs(["Friendly", "JSON"])

            with json_tab:
                st.json(result)

            with friendly_tab:
                st.markdown(ui_demo_logic.format_as_markdown(result))
