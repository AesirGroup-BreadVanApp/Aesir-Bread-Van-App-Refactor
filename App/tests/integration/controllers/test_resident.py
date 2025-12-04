import pytest
from App.controllers.resident import update_resident_username
from App.controllers.stop_request import request_stop, cancel_stop
from App.controllers.drive import schedule_drive
from App.models import StopRequest, Resident
from App.exceptions import ResourceNotFound, ValidationError


def test_request_stop(db_session, resident_user, driver_user, area, street):
    # Arrange
    drive = schedule_drive(
        driver_user.id, area.id, street.id, "2030-12-25", "10:00", "Scheduled", items=[]
    )
    message = "Please stop"

    # Act
    stop = request_stop(resident_user.id, drive.id, message)

    # Assert
    assert stop.resident_id == resident_user.id
    assert stop.drive_id == drive.id
    assert stop.message == message
    assert stop.id is not None


def test_request_stop_wrong_street(db_session, resident_user, driver_user, area):
    # Arrange
    from App.controllers.street import create_street

    other_street = create_street("Other Street", area.id)
    drive = schedule_drive(
        driver_user.id, area.id, other_street.id, "2030-12-25", "10:00", "Scheduled", items=[]
    )

    # Act & Assert
    with pytest.raises(ValidationError):
        request_stop(resident_user.id, drive.id, "Please stop")


def test_cancel_stop(db_session, resident_user, driver_user, area, street):
    # Arrange
    drive = schedule_drive(
        driver_user.id, area.id, street.id, "2030-12-25", "10:00", "Scheduled", items=[]
    )
    stop = request_stop(resident_user.id, drive.id, "Please stop")

    # Act
    result = cancel_stop(stop.id, resident_user.id)

    # Assert
    assert result is True
    assert StopRequest.query.get(stop.id) is None


def test_update_resident_username(db_session, resident_user):
    # Arrange
    new_username = "updatedresident"

    # Act
    result = update_resident_username(resident_user.id, new_username)

    # Assert
    assert result.username == new_username
    assert resident_user.username == new_username
