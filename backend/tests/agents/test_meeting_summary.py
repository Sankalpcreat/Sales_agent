import pytest
from agents.meeting_summary import MeetingSummaryAgent
from models.transcription import TranscriptionService
from models.ollama_request import OllamaApiClient


@pytest.fixture
def mock_transcription_service(mocker):
    mock_service = mocker.Mock(spec=TranscriptionService)
    mock_service.transcribe.return_value = "Client: We need cloud tools"
    return mock_service 

@pytest.fixture
def mock_ollama_api_client(mocker):
    mock_service = mocker.Mock(spec=OllamaApiClient)
    mock_service.query_model.return_value = "Summary: Client needs cloud tools"
    return mock_service

@pytest.fixture
def meeting_summary_agent(mock_transcription_service, mock_ollama_api_client):
    return MeetingSummaryAgent(mock_transcription_service, mock_ollama_api_client)

def test_summarize_meeting(meeting_summary_agent):
    audio_file = "test_audio.wav"
    result = meeting_summary_agent.summarize_meeting(audio_file)

    assert "Summary: Client needs cloud tools" in result