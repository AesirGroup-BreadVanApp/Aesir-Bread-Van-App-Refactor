from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.drive import (
    schedule_drive,
    start_drive,
    complete_drive,
    cancel_drive,
    view_drive,
    view_drives,
    get_drive_items,
    add_drive_item,
    remove_drive_item,
)
from App.controllers.driver import (
    update_driver_status,
    update_driver_username,
    update_area_info,
    update_street_info,
)
from App.exceptions import ResourceNotFound, ValidationError

driver_views = Blueprint("drive_views", __name__, template_folder="../templates")

def driver_required():
    if not current_user or current_user.role != 'driver':
        return False
    return True


@driver_views.route("/api/driver/schedule-drive", methods=["POST"])
@jwt_required()
def create_drive_api():
    if not driver_required():
        return jsonify(error="Forbidden"), 403

    data = request.json
    try:
        drive = schedule_drive(
            driver_id=current_user.id,
            area_id=data["area_id"],
            street_id=data["street_id"],
            date_str=data["date"],
            time_str=data["time"],
            status="Scheduled",
            items=data["items"],
        )
        return jsonify(drive.get_json()), 201
    except ValidationError as e:
        return jsonify(error=str(e)), 400


@driver_views.route("/api/driver/drives", methods=["GET"])
@jwt_required()
def get_drives_api():
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    try:
        drives = view_drives(current_user.id)
        return jsonify([drive.get_json() for drive in drives])
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404


@driver_views.route("/api/driver/drives/<int:drive_id>/start", methods=["PUT"])
@jwt_required()
def start_drive_api(drive_id):
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    try:
        drive = start_drive(current_user.id, drive_id)
        return jsonify(message="Drive started", drive=drive.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404


@driver_views.route("/api/driver/drives/<int:drive_id>/complete", methods=["PUT"])
@jwt_required()
def complete_drive_api(drive_id):
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    try:
        drive = complete_drive(current_user.id, drive_id)
        return jsonify(message="Drive completed", drive=drive.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@driver_views.route("/api/driver/drives/<int:drive_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_drive_api(drive_id):
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    try:
        drive = cancel_drive(current_user.id, drive_id)
        return jsonify(message="Drive cancelled", drive=drive.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
    

@driver_views.route("/api/driver/drives/<int:drive_id>/add-item", methods=["PUT"])
@jwt_required()
def add_drive_item_api(drive_id):
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    data = request.json
    try:
        drive_item = add_drive_item(current_user.id, drive_id, data["item_id"], data["quantity"])
        return jsonify(message="Drive item added", drive_item=drive_item.get_json()), 201
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
    except DuplicateEntity as e:
        return jsonify(error=str(e)), 409


@driver_views.route("/api/driver/drives/<int:drive_id>/remove-item", methods=["PUT"])
@jwt_required()
def remove_drive_item_api(drive_id):
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    data = request.json
    try:
        drive_item = remove_drive_item(current_user.id, drive_id, data["item_id"])
        return jsonify(message="Drive item removed", drive_item=drive_item.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404


@driver_views.route("/api/driver/status", methods=["PUT"])
@jwt_required()
def update_status_api():
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    data = request.json
    try:
        driver = update_driver_status(current_user.id, data["status"])
        return jsonify(message="Status updated", status=driver.status), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@driver_views.route("/api/driver/update-area", methods=["PUT"])
@jwt_required()
def update_area_api():
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    data = request.json
    try:
        driver = update_area_info(current_user.id, data["area_id"])
        return jsonify(message="Area updated", area=driver.area.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@driver_views.route("/api/driver/update-street", methods=["PUT"])
@jwt_required()
def update_street_api():
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    data = request.json
    try:
        driver = update_street_info(current_user.id, data["street_id"])
        return jsonify(message="Street updated", street=driver.street.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@driver_views.route("/api/driver/update-username", methods=["PUT"])
@jwt_required()
def update_username_api():
    if not driver_required():
        return jsonify(error="Forbidden"), 403
    data = request.json
    try:
        driver = update_driver_username(current_user.id, data["username"])
        username = driver.username
        return jsonify(message="Username updated", username=username), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
