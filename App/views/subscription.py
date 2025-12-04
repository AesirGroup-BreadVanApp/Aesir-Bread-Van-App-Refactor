from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.subscription import (
    subscribe_to_street,
    unsubscribe_from_street,
    view_subscriptions
)
from App.exceptions import ResourceNotFound, ValidationError

subscription_views = Blueprint('subscription_views', __name__, template_folder='../templates')

@subscription_views.route('/api/subscriptions', methods=['POST'])
@jwt_required()
def subscribe_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    
    data = request.json
    try:
        sub = subscribe_to_street(current_user.id, data['street_id'])
        return jsonify(message="Subscribed successfully", street_id=sub.street_id), 201
    except ValidationError as e:
        return jsonify(error=str(e)), 400

@subscription_views.route('/api/subscriptions', methods=['DELETE'])
@jwt_required()
def unsubscribe_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    data = request.json
    try:
        unsubscribe_from_street(current_user.id, data['street_id'])
        return jsonify(message="Unsubscribed successfully"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@subscription_views.route('/api/subscriptions', methods=['GET'])
@jwt_required()
def get_subscriptions_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    try:
        subs = view_subscriptions(current_user.id)
        return jsonify([sub.to_json() for sub in subs]), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
