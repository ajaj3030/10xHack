import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Legislation Explainer", layout="wide")

# Load data from CSV file
df = pd.read_csv("data/test_data.csv")

# Initialize state variables
if "section_dropdowns" not in st.session_state:
    st.session_state.section_dropdowns = {}

def create_section_dropdown(act, section, section_title):
    with st.expander(section_title, expanded=False):
        # Initialize state variables for this section dropdown
        if section_title not in st.session_state.section_dropdowns:
            st.session_state.section_dropdowns[section_title] = {
                "explanatory_notes": "",
                "explanatory_notes_approved": None,
                "redraft_prompt": ""
            }

        # Get the state variables for this section dropdown
        explanatory_notes = st.session_state.section_dropdowns[section_title]["explanatory_notes"]
        explanatory_notes_approved = st.session_state.section_dropdowns[section_title]["explanatory_notes_approved"]
        redraft_prompt = st.session_state.section_dropdowns[section_title]["redraft_prompt"]

        # Define the LLM function
        def generate_explanatory_notes(legislation):
            # Use a language model to generate explanatory notes
            explanatory_notes = f"The legislation states: {legislation}. This means that... [LLM-generated explanation]"
            return explanatory_notes

        def generate_explanatory_notes_with_redraft(legislation, original_notes, redraft_prompt):
            # Use the LLM to generate revised explanatory notes based on the redraft prompt
            revised_notes = f"The original explanatory notes were: {original_notes}. Based on the redraft prompt: '{redraft_prompt}', the revised explanatory notes are: [LLM-generated revised explanation]"
            return revised_notes

        def thumbs_up_callback():
            st.session_state.section_dropdowns[section_title]["explanatory_notes_approved"] = True

        def thumbs_down_callback():
            st.session_state.section_dropdowns[section_title]["explanatory_notes_approved"] = False

        def generate_notes_callback():
            # Reset the thumbs up/down buttons
            st.session_state.section_dropdowns[section_title]["explanatory_notes_approved"] = None
            st.session_state.section_dropdowns[section_title]["explanatory_notes"] = generate_explanatory_notes(legislation)

        col1, col2, col3, col4 = st.columns([0.8, 0.05, 0.05, 0.1])

        with col3:
            if st.button("👍", key=f"thumbs_up_{section_title}", on_click=thumbs_up_callback):
                pass

        with col4:
            if st.button("👎", key=f"thumbs_down_{section_title}", on_click=thumbs_down_callback):
                pass

        col5, col6 = st.columns(2)

        with col5:
            # The "Legislation" text area is now populated with the selected act and section
            legislation = df[(df["act"] == act) & (df["section"] == section)]["text"].iloc[0]
            st.text_area("Legislation", value=legislation, height=200)
            if st.button("Generate Explanatory Notes", key=f"generate_notes_{section_title}", on_click=generate_notes_callback):
                pass

        with col6:
            st.text_area("Explanatory Notes", value=explanatory_notes, height=200)
            if explanatory_notes_approved is True:
                st.success("Explanatory notes approved!", icon="✅")
            elif explanatory_notes_approved is False:
                redraft_prompt = st.text_input("Redraft Prompt", value=redraft_prompt, key=f"redraft_prompt_{section_title}", placeholder="Enter redraft prompt here")
                st.session_state.section_dropdowns[section_title]["redraft_prompt"] = redraft_prompt
                if redraft_prompt:
                    st.session_state.section_dropdowns[section_title]["explanatory_notes"] = generate_explanatory_notes_with_redraft(
                        legislation, explanatory_notes, redraft_prompt
                    )

# Streamlit UI
st.title("Legislation Explainer")

with st.sidebar:
    st.title("Select Act and Section")
    act_options = ["Please select ACT"] + list(df["act"].unique())
    selected_act = st.selectbox("Select Act", act_options)

    if selected_act == "Please select ACT":
        section_options = [""]
    else:
        section_options = ["Please select SECTION"] + list(df[df["act"] == selected_act]["section"].unique())
    selected_section = st.selectbox("Select Section", section_options)

if selected_act != "Please select ACT" and selected_section != "Please select SECTION":
    section_title = df[(df["act"] == selected_act) & (df["section"] == selected_section)]["section_title"].iloc[0]
    create_section_dropdown(selected_act, selected_section, section_title)