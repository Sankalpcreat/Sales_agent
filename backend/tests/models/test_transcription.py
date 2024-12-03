import pytest
import json
from unittest.mock import MagicMock, patch
from models.transcription import TranscriptionService


@pytest.fixture
def mock_vosk_model(mocker):
    mock_model = mocker.Mock()
    mocker.patch("models.transcription.Model", return_value=mock_model)
    return mock_model


@pytest.fixture
def mock_wave_open(mocker):
    mock_wave = mocker.patch("models.transcription.wave.open", create=True)
    return mock_wave


@pytest.fixture
def mock_kaldi_recognizer(mocker):
    mock_recognizer = mocker.Mock()
    mocker.patch("models.transcription.KaldiRecognizer", return_value=mock_recognizer)
    return mock_recognizer


def test_transcribe_success(mock_vosk_model, mock_wave_open, mock_kaldi_recognizer):
    mock_wave_file = MagicMock()
    mock_wave_file.getnchannels.return_value = 1
    mock_wave_file.getsampwidth.return_value = 2
    mock_wave_file.getcomptype.return_value = "NONE"
    mock_wave_file.readframes.side_effect = [b"data", b"data", b""]
    mock_wave_file.getframerate.return_value = 16000
    mock_wave_open.return_value.__enter__.return_value = mock_wave_file

    mock_kaldi_recognizer.AcceptWaveform.side_effect = [True, False]
    mock_kaldi_recognizer.Result.side_effect = [
        json.dumps({"text": "hello world"}),
        json.dumps({"text": ""}),
    ]
    mock_kaldi_recognizer.FinalResult.return_value = json.dumps({"text": "final result"})

    transcription_service = TranscriptionService(model_path="mock_path")
    result = transcription_service.transcribe("test_audio.wav")

    assert result == "hello world final result"


def test_transcribe_invalid_audio_format(mock_vosk_model, mock_wave_open):
    mock_wave_file = MagicMock()
    mock_wave_file.getnchannels.return_value = 2 
    mock_wave_open.return_value.__enter__.return_value = mock_wave_file

    transcription_service = TranscriptionService(model_path="mock_path")
    result = transcription_service.transcribe("test_audio.wav")

    assert "Audio file must be mono PCM WAV format." in result


def test_transcribe_exception_handling(mock_vosk_model, mock_wave_open):
    mock_wave_open.side_effect = Exception("Test exception")

    transcription_service = TranscriptionService(model_path="mock_path")
    result = transcription_service.transcribe("test_audio.wav")

    assert "Error during transcription: Test exception" in result


def test_file_existence():
    import os
    assert os.path.isfile("backend/tests/models/test_transcription.py")


def test_import_statements():
    import importlib
    try:
        importlib.import_module("models.transcription")
        importlib.import_module("unittest.mock")
        importlib.import_module("pytest")
        importlib.import_module("json")
    except ImportError as e:
        pytest.fail(f"Import error: {str(e)}")