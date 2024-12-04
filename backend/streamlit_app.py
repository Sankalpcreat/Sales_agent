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
from agents.proposal_drafting import ProposalDraftingAgent

# Determine Vosk model path
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vosk_model')

def initialize_system():
    """
    Initialize the entire AI sales assistant system
    Creates shared memory and connects all agents
    """
    # Initialize core services
    shared_memory = SharedMemoryService(vector_size=768)
    ollama_client = OllamaApiClient()
    transcription_service = TranscriptionService(model_path=VOSK_MODEL_PATH)

    # Initialize agents with shared memory
    meeting_agent = MeetingSummaryAgent(shared_memory, ollama_client, transcription_service)
    lead_agent = LeadSuggestionsAgent(shared_memory, ollama_client)
    proposal_agent = ProposalDraftingAgent(shared_memory, ollama_client)

    # Initialize orchestrator
    orchestrator = CentralOrchestrator()
    orchestrator.agents[TaskType.MEETING_SUMMARY] = meeting_agent
    orchestrator.agents[TaskType.LEAD_RECOMMENDATION] = lead_agent
    orchestrator.agents[TaskType.PROPOSAL_DRAFTING] = proposal_agent

    return orchestrator, shared_memory

def display_shared_memory(shared_memory):
    """
    Visualize the contents of shared memory
    """
    st.sidebar.header("Shared Memory Contents")
    
    # Retrieve and display contexts
    contexts = [
        "latest_meeting_summary", 
        "latest_lead_suggestions", 
        "latest_proposal_context"
    ]
    
    for context_key in contexts:
        context = shared_memory.get_context(context_key)
        if context:
            with st.sidebar.expander(f"{context_key.replace('_', ' ').title()}"):
                st.json(context)

def main():
    st.title("🚀 AI Sales Assistant Workflow")
    
    # Initialize system
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator, st.session_state.shared_memory = initialize_system()
    
    # Workflow steps
    workflow_steps = [
        "Meeting Summary", 
        "Lead Suggestions", 
        "Proposal Drafting"
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
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_file.getbuffer())
                temp_path = temp_audio.name
            
            # Process meeting summary
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
                
                # Clean up temporary file
                os.unlink(temp_path)
            
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    
    elif selected_step == "Lead Suggestions":
        st.header("🎯 Lead Generation")
        
        # Get meeting context from shared memory
        meeting_context = st.session_state.shared_memory.get_context('latest_meeting_summary')
        
        if meeting_context:
            st.subheader("Previous Meeting Context")
            st.json(meeting_context)
        
        requirements = st.text_area(
            "Enter additional requirements or context for lead generation", 
            height=200
        )
        
        if st.button("Generate Lead Suggestions"):
            try:
                result = st.session_state.orchestrator.execute_task({
                    "requirements": requirements,
                    "task": TaskType.LEAD_RECOMMENDATION,
                    "source": "lead_generation_step"
                })
                
                if result['status'] == 'success':
                    st.success("Lead Suggestions Generated!")
                    st.write(result.get('suggestions', 'No suggestions available'))
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")
            
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    
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
from agents.proposal_drafting import ProposalDraftingAgent

# Determine Vosk model path
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vosk_model')

def initialize_system():
    """
    Initialize the entire AI sales assistant system
    Creates shared memory and connects all agents
    """
    # Initialize core services
    shared_memory = SharedMemoryService(vector_size=768)
    ollama_client = OllamaApiClient()
    transcription_service = TranscriptionService(model_path=VOSK_MODEL_PATH)

    # Initialize agents with shared memory
    meeting_agent = MeetingSummaryAgent(shared_memory, ollama_client, transcription_service)
    lead_agent = LeadSuggestionsAgent(shared_memory, ollama_client)
    proposal_agent = ProposalDraftingAgent(shared_memory, ollama_client)

    # Initialize orchestrator
    orchestrator = CentralOrchestrator()
    orchestrator.agents[TaskType.MEETING_SUMMARY] = meeting_agent
    orchestrator.agents[TaskType.LEAD_RECOMMENDATION] = lead_agent
    orchestrator.agents[TaskType.PROPOSAL_DRAFTING] = proposal_agent

    return orchestrator, shared_memory

def display_shared_memory(shared_memory):
    """
    Visualize the contents of shared memory
    """
    st.sidebar.header("Shared Memory Contents")
    
    # Retrieve and display contexts
    contexts = [
        "latest_meeting_summary", 
        "latest_lead_suggestions", 
        "latest_proposal_context"
    ]
    
    for context_key in contexts:
        context = shared_memory.get_context(context_key)
        if context:
            with st.sidebar.expander(f"{context_key.replace('_', ' ').title()}"):
                st.json(context)

def main():
    st.title("🚀 AI Sales Assistant Workflow")
    
    # Initialize system
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator, st.session_state.shared_memory = initialize_system()
    
    # Workflow steps
    workflow_steps = [
        "Meeting Summary", 
        "Lead Suggestions", 
        "Proposal Drafting"
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
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_file.getbuffer())
                temp_path = temp_audio.name
            
            # Process meeting summary
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
                
                # Clean up temporary file
                os.unlink(temp_path)
            
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    
    elif selected_step == "Lead Suggestions":
        st.header("🎯 Lead Generation")
        
        # Get meeting context from shared memory
        meeting_context = st.session_state.shared_memory.get_context('latest_meeting_summary')
        
        if meeting_context:
            st.subheader("Previous Meeting Context")
            st.json(meeting_context)
        
        requirements = st.text_area(
            "Enter additional requirements or context for lead generation", 
            height=200
        )
        
        if st.button("Generate Lead Suggestions"):
            try:
                result = st.session_state.orchestrator.execute_task({
                    "requirements": requirements,
                    "task": TaskType.LEAD_RECOMMENDATION,
                    "source": "lead_generation_step"
                })
                
                if result['status'] == 'success':
                    st.success("Lead Suggestions Generated!")
                    st.write(result.get('suggestions', 'No suggestions available'))
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")
            
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    
    elif selected_step == "Proposal Drafting":
        st.header("📄 Proposal Generation")
        
        # Retrieve context from shared memory
        meeting_context = st.session_state.shared_memory.get_context('latest_meeting_summary')
        lead_context = st.session_state.shared_memory.get_context('latest_lead_suggestions')
        
        # Display previous contexts in expandable sections
        with st.expander("Meeting Context", expanded=False):
            if meeting_context:
                st.json(meeting_context)
            else:
                st.info("No meeting context available")
        
        with st.expander("Lead Suggestions Context", expanded=False):
            if lead_context:
                st.json(lead_context)
            else:
                st.info("No lead suggestions available")
        
        requirements = st.text_area(
            "Enter proposal requirements or additional context", 
            height=200
        )
        
        if st.button("Draft Proposal"):
            with st.spinner("Generating proposal..."):
                try:
                    result = st.session_state.orchestrator.execute_task({
                        "requirements": requirements,
                        "task": TaskType.PROPOSAL_DRAFTING,
                        "source": "proposal_drafting_step"
                    })
                    
                    if result['status'] == 'success' and result.get('proposal'):
                        st.success("Proposal Draft Generated!")
                        
                        # Display the proposal in a nicely formatted way
                        st.markdown("### Generated Proposal")
                        st.markdown(result['proposal'])
                        
                        # Add download button for the proposal
                        proposal_text = result['proposal']
                        st.download_button(
                            label="Download Proposal",
                            data=proposal_text,
                            file_name="techcorp_proposal.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error(f"Error: {result.get('message', 'Failed to generate proposal')}")
                
                except Exception as e:
                    st.error(f"Unexpected error while generating proposal: {str(e)}")


if __name__ == "__main__":
    main()