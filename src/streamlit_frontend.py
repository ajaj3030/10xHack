import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Legislation Explainer", layout="wide")

# Load data from CSV file
df = pd.read_csv("data/test_data.csv")

# Initialize state variables
if "explanatory_notes" not in st.session_state:
    st.session_state.explanatory_notes = ""

if "explanatory_notes_approved" not in st.session_state:
    st.session_state.explanatory_notes_approved = None

redraft_prompt = ""

# Define the LLM function
def generate_explanatory_notes(legislation):
    # Use a language model to generate explanatory notes
    explanatory_notes = f"The legislation states: {legislation}. This means that... [LLM-generated explanation]"
    return explanatory_notes

def generate_explanatory_notes_with_redraft(legislation, original_notes, redraft_prompt):
    # Use the LLM to generate revised explanatory notes based on the redraft prompt
    revised_notes = f"The original explanatory notes were: {original_notes}. Based on the redraft prompt: '{redraft_prompt}', the revised explanatory notes are: [LLM-generated revised explanation]"
    return revised_notes

# Streamlit UI
st.title("Legislation Explainer")

# Sidebar
with st.sidebar:
    st.title("Select Act and Section")
    act_options = ["Please select ACT"] + list(df["act"].unique())
    selected_act = st.selectbox("Select Act", act_options)

    if selected_act == "Please select ACT":
        section_options = [""]
    else:
        section_options = ["Please select SECTION"] + list(df[df["act"] == selected_act]["section"].unique())
    selected_section = st.selectbox("Select Section", section_options)

    # Populate the "Legislation" text area with the corresponding text
    if selected_act != "Please select ACT" and selected_section != "Please select SECTION":
        legislation = df[(df["act"] == selected_act) & (df["section"] == selected_section)]["text"].iloc[0]
    else:
        legislation = ""

col1, col2, col3, col4 = st.columns([0.8, 0.05, 0.05, 0.1])

with col3:
    if st.button("👍", key="thumbs_up"):
        st.session_state.explanatory_notes_approved = True

with col4:
    if st.button("👎", key="thumbs_down"):
        st.session_state.explanatory_notes_approved = False

col5, col6 = st.columns(2)

with col5:
    # The "Legislation" text area is now populated with the selected act and section
    st.text_area("Legislation", value=legislation, height=200)
    if st.button("Generate Explanatory Notes"):
        # Reset the thumbs up/down buttons
        st.session_state.explanatory_notes_approved = None
        st.session_state.explanatory_notes = generate_explanatory_notes(legislation)

with col6:
    st.text_area("Explanatory Notes", value=st.session_state.explanatory_notes, height=200)
    if st.session_state.explanatory_notes_approved is True:
        st.success("Explanatory notes approved!", icon="✅")
    elif st.session_state.explanatory_notes_approved is False:
        redraft_prompt = st.text_input("Redraft Prompt", value="", key="redraft_prompt", placeholder="Enter redraft prompt here")
        if redraft_prompt:
            st.session_state.explanatory_notes = generate_explanatory_notes_with_redraft(
                legislation, st.session_state.explanatory_notes, redraft_prompt
            )