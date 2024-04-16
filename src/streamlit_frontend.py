import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Legislation Explainer", layout="wide")

# Load data from CSV file
df = pd.read_csv("data/test_data.csv")

# Initialize state variables
if "section_dropdowns" not in st.session_state:
    st.session_state.section_dropdowns = {}

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

if "selected_option_left" not in st.session_state:
    st.session_state.selected_option_left = "Select an option"

if "selected_option_right" not in st.session_state:
    st.session_state.selected_option_right = "Select an option"

def create_section_dropdown(act, section, section_title):
    section_key = f"{act}_{section}_{section_title.replace(' ', '_')}"  # Generate a unique key
    
    with st.expander(section_title, expanded=False):
        # Initialize state variables for this section dropdown
        if section_key not in st.session_state.section_dropdowns:
            st.session_state.section_dropdowns[section_key] = {
                "explanatory_notes": "",
                "explanatory_notes_approved": None,
                "redraft_prompt": ""
            }

        # Get the state variables for this section dropdown
        explanatory_notes = st.session_state.section_dropdowns[section_key]["explanatory_notes"]
        explanatory_notes_approved = st.session_state.section_dropdowns[section_key]["explanatory_notes_approved"]
        redraft_prompt = st.session_state.section_dropdowns[section_key]["redraft_prompt"]

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
            st.session_state.section_dropdowns[section_key]["explanatory_notes_approved"] = True

        def thumbs_down_callback():
            st.session_state.section_dropdowns[section_key]["explanatory_notes_approved"] = False

        def generate_notes_callback():
            # Reset the thumbs up/down buttons
            st.session_state.section_dropdowns[section_key]["explanatory_notes_approved"] = None
        
            # Get the legislation text
            legislation = df[(df["act"] == act) & (df["section"] == section)]["text"].iloc[0]
        
            # Check if there's a redraft prompt
            redraft_prompt = st.session_state.section_dropdowns[section_key]["redraft_prompt"]
            if redraft_prompt:
                # Generate explanatory notes with redraft
                st.session_state.section_dropdowns[section_key]["explanatory_notes"] = generate_explanatory_notes_with_redraft(
                    legislation, st.session_state.section_dropdowns[section_key]["explanatory_notes"], redraft_prompt
                )
            else:
                # Generate explanatory notes without redraft
                st.session_state.section_dropdowns[section_key]["explanatory_notes"] = generate_explanatory_notes(legislation)

        col1, col2, col3, col4 = st.columns([0.8, 0.05, 0.05, 0.1])

        with col3:
            if st.button("👍", key=f"thumbs_up_{section_key}", on_click=thumbs_up_callback):
                pass

        with col4:
            if st.button("👎", key=f"thumbs_down_{section_key}", on_click=thumbs_down_callback):
                pass

        col5, col6 = st.columns(2)

        with col5:
            # The "Legislation" text area is now populated with the selected act and section
            legislation = df[(df["act"] == act) & (df["section"] == section)]["text"].iloc[0]
            st.text_area("Legislation", value=legislation, height=200)
            if st.button(label = "Generate ", key = f"Generate Explanatory Notes_{section_key}", on_click=generate_notes_callback):
                pass

        with col6:
            st.text_area(label = "Explanatory Notes", key = f"Explanatory Notes_{section_key}", value=explanatory_notes, height=200)
            if explanatory_notes_approved is True:
                st.success("Explanatory notes approved!", icon="✅")
            elif explanatory_notes_approved is False:
                redraft_prompt = st.text_input(label = "Redraft Prompt", key = f"Redraft Prompt_{section_key}", value=redraft_prompt, placeholder="Enter redraft prompt here")
                st.session_state.section_dropdowns[section_key]["redraft_prompt"] = redraft_prompt
                if redraft_prompt:
                    st.session_state.section_dropdowns[section_key]["explanatory_notes"] = generate_explanatory_notes_with_redraft(
                        legislation, explanatory_notes, redraft_prompt
                    )

# Streamlit UI
st.title("Legislation Explainer")

col1, col2 = st.columns(2)
with col1:
    selected_option_left = st.selectbox("How would you like to share your draft Legislation?", ["Select an option", "Download PDF", "Download DOCX", "Email"], key="selected_option_left")
with col2:
    selected_option_right = st.selectbox("How would you like to share your Explanatory Notes?", ["Select an option", "Download PDF", "Download DOCX", "Email"], key="selected_option_right")

with st.sidebar:
    st.title("Select Act and Section")
    act_options = ["Please select ACT"] + list(df["act"].unique())
    selected_act = st.selectbox("Select Act", act_options)

    if selected_act == "Please select ACT":
        section_options = ["Please select SECTION"]
    else:
        section_options = ["All"] + list(df[df["act"] == selected_act]["section"].unique())
    selected_section = st.selectbox("Select Section", section_options)

    # Add language selection dropdown
    language_options = ["English", "Welsh"]
    selected_language = st.selectbox("Select Language", language_options, index=0)
    st.session_state.selected_language = selected_language
    
    # Add audience level selection dropdown
    audience_level_options = ["No legal background", "Legal professional"]
    selected_audience_level = st.selectbox("Audience", audience_level_options, index=0)
    st.session_state.selected_audience_level = "1" if selected_audience_level == "No legal background" else "2"

if selected_act != "Please select ACT" and selected_section != "Please select SECTION":
    if selected_section == "All":
        sections_in_act = df[df["act"] == selected_act]["section"].unique()
        for section in sections_in_act:
            section_title = df[(df["act"] == selected_act) & (df["section"] == section)]["section_title"].iloc[0]
            create_section_dropdown(selected_act, section, section_title)
    else:
        section_title = df[(df["act"] == selected_act) & (df["section"] == selected_section)]["section_title"].iloc[0]
        create_section_dropdown(selected_act, selected_section, section_title)