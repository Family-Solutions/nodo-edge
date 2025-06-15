"""Interface services for the IAM bounded context."""
from flask import Blueprint, request, jsonify
from iam.application.services import AuthApplicationService

iam_api = Blueprint("iam_api", __name__)

# Initialize dependencies
auth_service = AuthApplicationService()

def authenticate_request():
    """Authenticate an incoming HTTP request.

    Checks for device_id in the JSON body and X-API-Key in headers.

    Returns:
        tuple: (JSON response, status code) if authentication fails, None if successful.
    """
    device_id = request.json.get("device_id") if request.json else None
    api_key = request.headers.get("X-API-Key")
    if not device_id or not api_key:
        return jsonify({"error": "Missing device_id or X-API-Key"}), 401
    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 401
    return None