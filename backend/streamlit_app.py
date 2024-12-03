import streamlit as st
import requests
import json
from pathlib import Path

st.set_page_config(
    page_title="Sales Agent Dashboard",
    page_icon="💼",
    layout="wide"
)

st.title("🤖 AI Sales Assistant Dashboard")

# API endpoint
API_URL = "http://localhost:8000/api"

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Meeting Summary", "Lead Suggestions", "Proposal", "Lead Scoring", "Follow Up"])

if page == "Meeting Summary":
    st.header("📝 Meeting Summary")
    uploaded_file = st.file_uploader("Upload audio file (WAV format)", type=['wav'])
    
    if uploaded_file is not None:
        if st.button("Generate Summary"):
            files = {"file": uploaded_file}
            with st.spinner("Generating summary..."):
                response = requests.post(f"{API_URL}/summarize", files=files)
                if response.status_code == 200:
                    summary = response.json()["summary"]
                    st.success("Summary generated successfully!")
                    st.text_area("Meeting Summary", summary, height=200)
                else:
                    st.error(f"Error: {response.text}")

elif page == "Lead Suggestions":
    st.header("🎯 Lead Suggestions")
    meeting_notes = st.text_area("Enter meeting notes", height=200)
    
    if st.button("Get Lead Suggestions"):
        with st.spinner("Analyzing notes..."):
            response = requests.post(f"{API_URL}/lead-suggestions", json={"notes": meeting_notes})
            if response.status_code == 200:
                suggestions = response.json()["suggestions"]
                st.success("Suggestions generated!")
                for idx, suggestion in enumerate(suggestions, 1):
                    st.write(f"{idx}. {suggestion}")
            else:
                st.error(f"Error: {response.text}")

elif page == "Proposal":
    st.header("📄 Proposal Generator")
    client_info = st.text_area("Enter client information and requirements", height=200)
    
    if st.button("Generate Proposal"):
        with st.spinner("Generating proposal..."):
            response = requests.post(f"{API_URL}/proposal", json={"client_info": client_info})
            if response.status_code == 200:
                proposal = response.json()["proposal"]
                st.success("Proposal generated!")
                st.text_area("Generated Proposal", proposal, height=300)
            else:
                st.error(f"Error: {response.text}")

elif page == "Lead Scoring":
    st.header("📊 Lead Scoring")
    lead_info = st.text_area("Enter lead information", height=200)
    
    if st.button("Score Lead"):
        with st.spinner("Analyzing lead..."):
            response = requests.post(f"{API_URL}/score-leads", json={"lead_info": lead_info})
            if response.status_code == 200:
                score = response.json()["score"]
                st.success(f"Lead Score: {score}/100")
                st.progress(score/100)
            else:
                st.error(f"Error: {response.text}")

else:  # Follow Up
    st.header("📨 Follow-up Generator")
    interaction_history = st.text_area("Enter interaction history", height=200)
    
    if st.button("Generate Follow-up"):
        with st.spinner("Generating follow-up message..."):
            response = requests.post(f"{API_URL}/follow-up", json={"history": interaction_history})
            if response.status_code == 200:
                message = response.json()["message"]
                st.success("Follow-up message generated!")
                st.text_area("Follow-up Message", message, height=200)
            else:
                st.error(f"Error: {response.text}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your Sales AI Assistant")