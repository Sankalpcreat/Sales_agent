import pytest
from core.orchestrator import Orchestrator

@pytest.fixture
def orchestrator():
    return Orchestrator()

@pytest.fixture
def mock_agent():
    def mock_workflow(data):
        return {"success": True, "data": data}
    return mock_workflow

def test_register_agent(orchestrator, mock_agent):
    orchestrator.register_agent("test_workflow", mock_agent)
    assert "test_workflow" in orchestrator.agent
    assert orchestrator.agent["test_workflow"] == mock_agent

def test_execute_workflow_success(orchestrator, mock_agent):
    orchestrator.register_agent("test_workflow", mock_agent)
    data = {"key": "value"}
    result = orchestrator.execute_workflow("test_workflow", data)
    assert result == {"success": True, "data": data}

def test_execute_workflow_not_registered(orchestrator):
    with pytest.raises(ValueError, match="Workflow test_workflow not registered."):
        orchestrator.execute_workflow("test_workflow", {"key": "value"})

def test_execute_workflow_error(orchestrator):
    def faulty_agent(data):
        raise Exception("Simulated error")
    
    orchestrator.register_agent("faulty_workflow", faulty_agent)
    result = orchestrator.execute_workflow("faulty_workflow", {"key": "value"})
    assert "Error executing workflow 'faulty_workflow': Simulated error" in str(result)