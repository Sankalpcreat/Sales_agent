import os
import tempfile
import streamlit as st
import json

from core.orchestrator import CentralOrchestrator, TaskType
from core.shared_memory import SharedMemoryService
from models.ollama_request import OllamaApiClient
from models.transcription import TranscriptionService

from agents.meeting_summary import MeetingSummaryAgent
from agents.lead_suggestions import LeadSuggestionsAgent

# Determine Vosk model path
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vosk_model')

def initialize_system():
    """
    Initialize the AI sales assistant system
    Creates shared memory and connects required agents
    """
    # Initialize core services
    shared_memory = SharedMemoryService(vector_size=768)
    ollama_client = OllamaApiClient()
    transcription_service = TranscriptionService(model_path=VOSK_MODEL_PATH)

    # Initialize agents
    meeting_agent = MeetingSummaryAgent(shared_memory, ollama_client, transcription_service)
    lead_agent = LeadSuggestionsAgent(shared_memory, ollama_client)

    # Initialize orchestrator
    orchestrator = CentralOrchestrator()
    orchestrator.agents[TaskType.MEETING_SUMMARY] = meeting_agent
    orchestrator.agents[TaskType.LEAD_RECOMMENDATION] = lead_agent

    return orchestrator, shared_memory

def display_shared_memory(shared_memory):
    """
    Visualize the contents of shared memory
    """
    st.sidebar.header("Shared Memory Contents")
    
    # Retrieve and display contexts
    contexts = [
        "latest_meeting_summary", 
        "latest_lead_suggestions"
    ]
    
    for context_key in contexts:
        context = shared_memory.get_context(context_key)
        if context:
            with st.sidebar.expander(f"{context_key.replace('_', ' ').title()}"):
                st.json(context)

def main():
    st.title("🚀 AI Sales Assistant")
    
    # Initialize system
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator, st.session_state.shared_memory = initialize_system()
    
    # Workflow steps
    workflow_steps = [
        "Meeting Summary", 
        "Lead Suggestions"
    ]
    
    # Sidebar for navigation
    selected_step = st.sidebar.radio("Workflow Steps", workflow_steps)
    
    # Display shared memory contents
    display_shared_memory(st.session_state.shared_memory)
    
    # Workflow implementation
    if selected_step == "Meeting Summary":
        st.header("📝 Meeting Transcription")
        
        # Audio file upload
        audio_file = st.file_uploader("Upload Meeting Recording", type=['wav'])
        
        if audio_file:
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
                    st.subheader("Transcript")
                    st.text(result.get('transcript', 'No transcript available'))
                    st.subheader("Summary")
                    st.write(result.get('summary', 'No summary available'))
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")
                
                os.unlink(temp_path)
            
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    
    elif selected_step == "Lead Suggestions":
        st.header("🎯 Lead Generation")
        
        # Create two columns
        left_col, right_col = st.columns([1, 1])
        
        with left_col:
            meeting_context = st.session_state.shared_memory.get_context('latest_meeting_summary')
            
            if meeting_context:
                with st.expander("Previous Meeting Context", expanded=False):
                    st.json(meeting_context)
            
            requirements = st.text_area(
                "Enter requirements for lead generation", 
                height=200
            )
            
            if st.button("Generate Lead Suggestions"):
                try:
                    result = st.session_state.orchestrator.execute_task({
                        "requirements": requirements,
                        "task": TaskType.LEAD_RECOMMENDATION,
                        "source": "lead_generation_step"
                    })
                    
                    # Store the result in session state
                    if result['status'] == 'success':
                        st.session_state.lead_suggestions = result.get('suggestions', 'No suggestions available')
                        st.success("Lead Suggestions Generated!")
                    else:
                        st.error(f"Error: {result.get('message', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        
        with right_col:
            st.subheader("Generated Suggestions")
            if 'lead_suggestions' in st.session_state:
                st.write(st.session_state.lead_suggestions)
            else:
                st.info("Generate leads to see suggestions here")

if __name__ == "__main__":
    main()