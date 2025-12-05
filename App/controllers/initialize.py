from App.database import db
from App.models import Admin, Item
from App.controllers.resident import create_resident
from App.controllers.driver import create_driver
from App.controllers.area import create_area
from App.controllers.street import create_street
from App.controllers.drive import add_drive_item, schedule_drive
from App.controllers.subscription import subscribe_to_street
from App.controllers.item import create_item
from App.models.enums import DriverStatus


def initialize():
    db.drop_all()
    db.create_all()

    # Create Admin
    admin = Admin("admin", "adminpass")
    db.session.add(admin)
    db.session.commit()
    print("Admin created: admin/adminpass")

    # Create area1
    area1 = create_area("Downtown")
    area2 = create_area("Middletown")
    print(f"Areas created: {area1.name}, {area2.name}")

    # Create Streets
    main_st = create_street("Main St", area1.id)
    first_ave = create_street("First Ave", area1.id)
    print(f"Streets created: {main_st.name} in {area1.name}, {first_ave.name} in {area1.name}")

    # Create Driver
    driver = create_driver("driver1", "driverpass", DriverStatus.OFF_DUTY.value, area1.id, first_ave.id)
    print(f"Driver created: {driver.username}/driverpass")

    # Create Resident
    resident = create_resident("resident1", "residentpass", area1.id, main_st.id, 101)
    print(f"Resident created: {resident.username}/residentpass")

    # Create Items
    bread = create_item(name="Bread", price=2.50, description="Fresh Bread", tags=[])
    croissant = create_item(
        name="Croissant", price=1.50, description="Buttery Croissant", tags=[]
    )
    bagel = create_item(name="Bagel", price=2.00, description="Fresh Bagel", tags=[])
    naan = create_item(name="Naan", price=1.00, description="Soft Naan", tags=[])
    pita_bread = create_item(
        name="Pita Bread", price=1.20, description="Whole Wheat Pita", tags=[]
    )
    cornbread = create_item(
        name="Cornbread", price=1.80, description="Sweet Cornbread", tags=[]
    )

    # Subscribe Resident to Main St
    subscribe_to_street(resident.id, main_st.id)
    print(f"Resident {resident.username} subscribed to {main_st.name}")

    # Schedule a Drive (triggers notification)
    drive = schedule_drive(
        driver_id=driver.id,
        area_id=area1.id,
        street_id=main_st.id,
        date_str="2025-12-26",
        time_str="10:00",
        status="Scheduled",
        items=[
            {"item_id": bread.id, "quantity": 5},
            {"item_id": croissant.id, "quantity": 3},
        ],
    )
    print(f"Drive scheduled on {main_st.name} at {drive.time}")

    db.session.commit()
