import pytest
from App.controllers.drive import schedule_drive, view_drives, add_drive_item
from App.models import Drive, Item, DriveItem
from datetime import datetime


def test_schedule_drive(db_session, driver_user, area, street):
    # Arrange
    date_str = "2026-12-25"
    time_str = "10:00"
    status = "Scheduled"
    # Act
    drive = schedule_drive(driver_user.id, area.id, street.id, date_str, time_str, status, items=[])

    # Assert
    assert drive.driver_id == driver_user.id
    assert drive.area_id == area.id
    assert drive.street_id == street.id
    assert drive.date == datetime.strptime(date_str, "%Y-%m-%d").date()
    assert drive.time == datetime.strptime(time_str, "%H:%M").time()
    assert drive.status == status
    assert drive.id is not None
    assert Drive.query.get(drive.id) is not None


def test_view_drives(db_session, driver_user, area, street):
    # Arrange
    schedule_drive(driver_user.id, area.id, street.id, "2026-12-25", "10:00", "Scheduled", items=[])
    schedule_drive(driver_user.id, area.id, street.id, "2026-12-26", "11:00", "Scheduled", items=[])

    # Act
    drives = view_drives(driver_user.id)

    # Assert
    assert len(drives) == 2


def test_add_drive_item(db_session, driver_user, area, street):
    # Arrange
    drive = schedule_drive(
        driver_user.id, area.id, street.id, "2026-12-25", "10:00", "Scheduled", items=[]
    )
    item = Item(name="Bread", price=2.50, description="Fresh Bread", tags=[])
    db_session.session.add(item)
    db_session.session.commit()

    # Act
    drive_item = add_drive_item(driver_user.id, drive.id, item.id, 10)

    # Assert
    assert drive_item.drive_id == drive.id
    assert drive_item.item_id == item.id
    assert drive_item.quantity == 10
    assert len(drive.items) == 1
