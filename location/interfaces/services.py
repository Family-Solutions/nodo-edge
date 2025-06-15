"""Interface services for the Location-bounded context."""
from flask import Blueprint, request, jsonify

from location.application.services.location_service import LocationRecordApplicationService
from iam.interfaces.services import authenticate_request

location_api = Blueprint("location_api", __name__)

# Inicializa el servicio de ubicación
location_service = LocationRecordApplicationService()

@location_api.route("/api/v1/location", methods=["POST"])
def create_location():
    """Handle POST requests to create a location record.

    Expects JSON with device_id, latitude, longitude, and optional created_at.

    Returns:
        tuple: (JSON response, status code).
    """
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        device_id = data["device_id"]
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        created_at = data.get("created_at")
        record = location_service.create_location_record(
            device_id, latitude, longitude, created_at, request.headers.get("X-API-Key")
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
