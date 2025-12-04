from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.resident import (
    update_area_info,
    update_street_info,
    update_house_number,
    update_resident_username,
)
from App.controllers.stop_request import (
    request_stop,
    get_requested_stops,
    cancel_stop
)
from App.controllers.driver import get_driver_status_and_location
from App.exceptions import ResourceNotFound, ValidationError, DuplicateEntity

resident_views = Blueprint('resident_views', __name__, template_folder='../templates')

@resident_views.route('/api/resident/stops', methods=['POST'])
@jwt_required()
def request_stop_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    
    data = request.json
    try:
        stop = request_stop(current_user.id, data['drive_id'], data['message'])
        return jsonify(stop.get_json()), 201
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
    except ValidationError as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/stops', methods=['GET'])
@jwt_required()
def get_stops_api():
    try:
        if current_user.role != 'resident':
            return jsonify(error="Forbidden"), 403
        
        stops = get_requested_stops(current_user.id)
        return jsonify([stop.get_json() for stop in stops]), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@resident_views.route('/api/resident/stops/<int:stop_id>', methods=['DELETE'])
@jwt_required()
def cancel_stop_api(stop_id):
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    try:
        cancel_stop(stop_id, current_user.id)
        return jsonify(message="Stop request cancelled"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
    except ValidationError as e:
        return jsonify(error=str(e)), 400

@resident_views.route('/api/resident/area', methods=['PUT'])
@jwt_required()
def update_area_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    
    data = request.json
    try:
        resident = update_area_info(current_user.id, data['area_id'])
        area = resident.area
        return jsonify(message=f"Area name updated to {area}", area=area.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@resident_views.route('/api/resident/street', methods=['PUT'])
@jwt_required()
def update_street_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    
    data = request.json
    try:
        resident = update_street_info(current_user.id, data['street_id'])
        street = resident.street
        return jsonify(message=f"Street name updated to {street}", street=street.get_json()), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@resident_views.route('/api/resident/house_number', methods=['PUT'])
@jwt_required()
def update_house_number_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    
    data = request.json
    try:
        resident = update_house_number(current_user.id, data['house_number'])
        house_number = resident.house_number
        return jsonify(message=f"House number updated to {house_number}"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@resident_views.route('/api/resident/username', methods=['PUT'])
@jwt_required()
def update_username_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    
    data = request.json
    try:
        resident = update_resident_username(current_user.id, data['username'])
        username = resident.username
        return jsonify(message=f"Username updated to {username}", username=username), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@resident_views.route('/api/resident/get-driver-status/<int:driver_id>', methods=['GET'])
@jwt_required()
def get_driver_status_api(driver_id):
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    try:
        driver_status = get_driver_status_and_location(driver_id)
        return jsonify(message="Driver status retrieved", driver_status=driver_status), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404