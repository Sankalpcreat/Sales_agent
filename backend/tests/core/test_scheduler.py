import pytest
from core.scheduler import SchedulerService


@pytest.fixture
def scheduler_service():
    
    return SchedulerService()


def test_add_job(scheduler_service, mocker):
   
    mock_add_job = mocker.patch.object(scheduler_service.scheduler, "add_job")
    mock_func = mocker.Mock()

    scheduler_service.add_job(mock_func, trigger="interval", seconds=10)

    
    mock_add_job.assert_called_once_with(mock_func, trigger="interval", seconds=10)


def test_scheduler_start(scheduler_service, mocker):
    
    mock_start = mocker.patch.object(scheduler_service.scheduler, "start")

    scheduler_service.start()

    # Verify that the start method is called
    mock_start.assert_called_once()