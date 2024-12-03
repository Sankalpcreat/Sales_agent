import pytest
from agents.follow_up import FollowUpAgent
from core.scheduler import SchedulerService

@pytest.fixture
def mock_scheduler_service(mocker):
    mock_service=mocker.Mock(spec=SchedulerService)
    return mock_service

@pytest.fixture
def follow_up_agent(mock_scheduler_service):
    return FollowUpAgent(mock_scheduler_service)

def test_schedule_follow_up(follow_up_agent, mock_scheduler_service):
    lead_id = 1
    follow_up_time = "2024-12-05T10:00:00"
    message = "Follow-up with Acme Corp"

    follow_up_agent.schedule_follow_up(lead_id, follow_up_time, message)


    mock_scheduler_service.add_job.assert_called_once()
    call_args = mock_scheduler_service.add_job.call_args
    assert call_args.kwargs['trigger'] == 'date'
    assert call_args.kwargs['run_date'] == follow_up_time
