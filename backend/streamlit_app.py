import os
import tempfile
import streamlit as st
from core.orchestrator import CentralOrchestrator, TaskType
from core.shared_memory import SharedMemoryService
from models.ollama_request import OllamaApiClient
from models.transcription import TranscriptionService
from agents.meeting_summary import MeetingSummaryAgent
from agents.lead_suggestions import LeadSuggestionsAgent

VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vosk_model')

def initialize_system():
    shared_memory = SharedMemoryService(vector_size=768)
    ollama_client = OllamaApiClient()
    transcription_service = TranscriptionService(model_path=VOSK_MODEL_PATH)
    meeting_agent = MeetingSummaryAgent(shared_memory, ollama_client, transcription_service)
    lead_agent = LeadSuggestionsAgent(shared_memory, ollama_client)
    orchestrator = CentralOrchestrator()
    orchestrator.agents[TaskType.MEETING_SUMMARY] = meeting_agent
    orchestrator.agents[TaskType.LEAD_RECOMMENDATION] = lead_agent
    return orchestrator, shared_memory

def display_shared_memory(shared_memory):
    st.sidebar.header("Shared Memory Contents", help="This section displays the latest context from previous operations.")
    contexts = ["latest_meeting_summary", "latest_lead_suggestions"]
    for context_key in contexts:
        context = shared_memory.get_context(context_key)
        if context:
            with st.sidebar.expander(f"{context_key.replace('_', ' ').title()}", expanded=False):
                st.json(context)

def meeting_summary_ui():
    st.header("📝 Meeting Transcription and Summary")
    audio_file = st.file_uploader("Upload Meeting Recording (WAV format)", type=['wav'], help="Upload a WAV file of your meeting recording.")
    if audio_file:
        with st.spinner("Processing audio..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_file.getbuffer())
                temp_path = temp_audio.name
            try:
                result = st.session_state.orchestrator.execute_task({
                    "audio_path": temp_path,
                    "task": TaskType.MEETING_SUMMARY,
                    "source": "streamlit_upload"
                })
                if result['status'] == 'success':
                    st.success("Meeting Summarized Successfully!")
                    with st.expander("Transcript", expanded=False):
                        st.text(result.get('transcript', 'No transcript available'))
                    st.subheader("Summary")
                    st.write(result.get('summary', 'No summary available'))
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")
                os.unlink(temp_path)
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

def lead_suggestions_ui():
    st.header("🎯 Lead Generation")
    col1, col2 = st.columns([3, 2])
    with col1:
        meeting_context = st.session_state.shared_memory.get_context('latest_meeting_summary')
        if meeting_context:
            with st.expander("Previous Meeting Context", expanded=False):
                st.json(meeting_context)
        requirements = st.text_area("Enter requirements for lead generation", 
                                    height=150, 
                                    help="Specify your requirements for potential leads.")
        if st.button("Generate Lead Suggestions", type="primary"):
            with st.spinner("Generating leads..."):
                try:
                    result = st.session_state.orchestrator.execute_task({
                        "requirements": requirements,
                        "task": TaskType.LEAD_RECOMMENDATION,
                        "source": "lead_generation_step"
                    })
                    if result['status'] == 'success':
                        st.session_state.lead_suggestions = result.get('suggestions', 'No suggestions available')
                        st.success("Lead Suggestions Generated!")
                    else:
                        st.error(f"Error: {result.get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")
    
    with col2:
        st.subheader("Generated Suggestions")
        if 'lead_suggestions' in st.session_state:
            st.markdown(st.session_state.lead_suggestions)
        else:
            st.info("Generate leads to see suggestions here")

def main():
    st.set_page_config(page_title="AI Sales Assistant", page_icon="🚀", layout="wide")
    st.title("🚀 AI Sales Assistant")
    
    if 'orchestrator' not in st.session_state:
        with st.spinner("Initializing system..."):
            st.session_state.orchestrator, st.session_state.shared_memory = initialize_system()
    
    workflow_steps = ["Meeting Summary", "Lead Suggestions"]
    selected_step = st.sidebar.radio("Workflow Steps", workflow_steps)
    
    display_shared_memory(st.session_state.shared_memory)
    
    if selected_step == "Meeting Summary":
        meeting_summary_ui()
    elif selected_step == "Lead Suggestions":
        lead_suggestions_ui()

if __name__ == "__main__":
    main()