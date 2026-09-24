"""The presentation layer for the streamlit app"""

import streamlit as st  # all streamlit commands will be available through the "st" alias
from data_storyteller import ui_demo_logic  # reference to local logic script

st.set_page_config(page_title="Data Storyteller", layout="wide")  # HTML title
st.title("Data Storyteller")  # page title


def render_table(table_block):
    st.header(table_block["table_heading"])
    st.dataframe(data=table_block["table"], width="content")
    st.caption(table_block["table_caption"])


def render_image(image_block):
    left_spacer, img_col, right_spacer = st.columns(spec=[0.2, 0.6, 0.2])

    with img_col:
        st.image(image_block["image_file_name"], caption=image_block["accessible_caption"])


def render_commentary(text_block):
    st.header(text_block["section_heading"])
    st.write(text_block["commentary"])


def render_error(error_block):
    st.header("Error")
    st.write(error_block["error_message"])


def render_source_data(source_data_block):
    st.header("Source Data")
    with st.expander("Source Data"):
        st.json(source_data_block)


report_topic = st.text_input(
    "Report to generate:",
    value="Write a brief report on our EU sales data. The first visualization should be a pie chart showing unit sales by country.",
)

run_button = st.button("Run")

if run_button:
    with st.spinner("Thinking...."):
        report = ui_demo_logic.generate_report(report_topic)

        for item in report:
            content_type = item["content_type"]

            if content_type == "commentary":
                render_commentary(item)
            elif content_type == "chart":
                render_image(item)
            elif content_type == "table":
                render_table(item)
            elif content_type == "error":
                render_error(item)
            elif content_type == "source_data":
                render_source_data(item)
            else:
                st.write(f"INVALID CONTENT TYPE: {content_type}")
