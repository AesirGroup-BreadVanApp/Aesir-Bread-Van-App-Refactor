from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.notification import get_notification_history_json, mark_notification_as_read
from App.exceptions import ResourceNotFound, ValidationError
notification_views = Blueprint('notification_views', __name__, template_folder='../templates')

@notification_views.route('/api/notifications', methods=['GET'])
@jwt_required()
def get_notifications_api():
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    try:
        notifications = get_notification_history_json(current_user.id)
        return jsonify(notifications), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404

@notification_views.route('/api/notifications/<int:notification_id>', methods=['PUT'])
@jwt_required()
def mark_notification_as_read_api(notification_id):
    if current_user.role != 'resident':
        return jsonify(error="Forbidden"), 403
    try:
        mark_notification_as_read(notification_id, current_user.id)
        return jsonify(message="Notification marked as read"), 200
    except ResourceNotFound as e:
        return jsonify(error=str(e)), 404
    except ValidationError as e:
        return jsonify(error=str(e)), 400
