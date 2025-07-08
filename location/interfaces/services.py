"""Interface services for the Location-bounded context."""
from flask import Blueprint, request, jsonify
import requests
from datetime import datetime

from location.application.services.location_service import LocationRecordApplicationService

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
    # Try multiple ways to get JSON data
    data = None
    try:
        # First try standard JSON
        if request.is_json:
            data = request.json
        else:
            # Try to parse as JSON regardless of content-type
            import json
            raw_data = request.get_data(as_text=True)
            if raw_data:
                data = json.loads(raw_data)
    except Exception as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400

    if not data:
        return jsonify({"error": "Empty request body"}), 400
        
    try:
        device_id = data["device_id"]
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        created_at = data.get("created_at")
        record = location_service.create_location_record(
            device_id, latitude, longitude, created_at
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

@location_api.route("/api/v1/locations", methods=["GET"])
def get_all_locations():
    """Handle GET requests to retrieve all location records.

    Returns:
        tuple: (JSON response, status code).
    """
    print("GET /api/v1/locations - Request received")

    try:
        print("Getting all location records...")
        records = location_service.get_all_location_records()
        print(f"Found {len(records)} location records")
        
        result = []
        for record in records:
            result.append({
                "id": record.id,
                "device_id": record.device_id,
                "latitude": record.latitude,
                "longitude": record.longitude,
                "created_at": record.created_at.isoformat() + "Z"
            })
        
        print("Returning JSON response...")
        return jsonify(result), 200
    except Exception as e:
        print(f"Error in get_all_locations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@location_api.route("/api/v1/sync-external", methods=["POST"])
def sync_external_locations():
    """Sync locations from external API.
    
    Gets data from https://inuest.pythonanywhere.com/api/v1/locations
    and creates/updates local records based on device_id existence.
    
    Returns:
        tuple: (JSON response, status code).
    """
    print("POST /api/v1/sync-external - Starting external sync")
    
    external_api_url = "https://inuest.pythonanywhere.com/api/v1/locations"
    
    try:
        # Get data from external API
        print(f"Fetching data from {external_api_url}")
        response = requests.get(external_api_url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({
                "error": f"External API returned {response.status_code}",
                "details": response.text
            }), 502
        
        external_locations = response.json()
        print(f"Retrieved {len(external_locations)} locations from external API")
        
        if not external_locations:
            return jsonify({
                "message": "No locations found in external API",
                "created": 0,
                "updated": 0
            }), 200
        
        created_count = 0
        updated_count = 0
        errors = []
        
        # Process each location
        for location_data in external_locations:
            try:
                device_id = location_data["device_id"]
                latitude = float(location_data["latitude"])
                longitude = float(location_data["longitude"])
                created_at = location_data["created_at"]
                
                # Check if device_id already exists
                existing_record = location_service.find_by_device_id(device_id)
                
                if existing_record is None:
                    # Device doesn't exist - CREATE (POST)
                    print(f"Creating new record for device_id: {device_id}")
                    location_service.create_location_record(device_id, latitude, longitude, created_at)
                    created_count += 1
                else:
                    # Device exists - UPDATE (PUT)
                    print(f"Updating existing record for device_id: {device_id}")
                    location_service.update_location_record(device_id, latitude, longitude, created_at)
                    updated_count += 1
                    
            except KeyError as e:
                error_msg = f"Missing required field in location data: {str(e)}"
                print(f"Error: {error_msg}")
                errors.append(error_msg)
            except ValueError as e:
                error_msg = f"Invalid data format for device {device_id}: {str(e)}"
                print(f"Error: {error_msg}")
                errors.append(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error processing device {device_id}: {str(e)}"
                print(f"Error: {error_msg}")
                errors.append(error_msg)
        
        # Prepare response
        response_data = {
            "message": "Sync completed",
            "total_processed": len(external_locations),
            "created": created_count,
            "updated": updated_count,
            "errors": len(errors)
        }
        
        if errors:
            response_data["error_details"] = errors
        
        print(f"Sync completed: {created_count} created, {updated_count} updated, {len(errors)} errors")
        return jsonify(response_data), 200
        
    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout connecting to external API"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to external API: {str(e)}"}), 502
    except Exception as e:
        print(f"Unexpected error in sync_external_locations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@location_api.route("/api/v1/sync-to-collar", methods=["POST"])
def sync_to_collar_api():
    """Sync local location records to collar API.
    
    Gets all local location records and sends them to collar API
    at http://localhost:8080/api/v1/collar/updateLocation/{device_id}
    
    Returns:
        tuple: (JSON response, status code).
    """
    print("POST /api/v1/sync-to-collar - Starting collar API sync")
    
    collar_api_base_url = "http://localhost:8080/api/v1/collar/updateLocation"
    
    try:
        # Get all local location records
        print("Getting all local location records...")
        local_records = location_service.get_all_location_records()
        print(f"Found {len(local_records)} local location records")
        
        if not local_records:
            return jsonify({
                "message": "No local location records found",
                "sent": 0,
                "errors": 0
            }), 200
        
        # Group by device_id to get the latest location for each device
        device_locations = {}
        for record in local_records:
            device_id = record.device_id
            created_at = record.created_at
            
            # Keep only the most recent record for each device
            if device_id not in device_locations or created_at > device_locations[device_id]["created_at"]:
                device_locations[device_id] = {
                    "latitude": record.latitude,
                    "longitude": record.longitude,
                    "created_at": created_at
                }
        
        print(f"Processing latest locations for {len(device_locations)} unique devices")
        
        sent_count = 0
        errors = []
        
        # Send each device's latest location to collar API
        for device_id, location_data in device_locations.items():
            try:
                # Prepare the URL and payload
                url = f"{collar_api_base_url}/{device_id}"
                payload = {
                    "serialNumber": device_id,
                    "lastLatitude": location_data["latitude"],
                    "lastLongitude": location_data["longitude"]
                }
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                print(f"Sending location update for device {device_id} to {url}")
                
                # Send PUT request to collar API
                response = requests.put(url, json=payload, headers=headers, timeout=10)
                
                if response.status_code in [200, 201, 204]:
                    print(f"✅ Successfully sent location for device {device_id}")
                    sent_count += 1
                else:
                    error_msg = f"Error sending location for device {device_id}: {response.status_code} - {response.text}"
                    print(f"❌ {error_msg}")
                    errors.append(error_msg)
                    
            except requests.exceptions.Timeout:
                error_msg = f"Timeout sending location for device {device_id}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
            except requests.exceptions.RequestException as e:
                error_msg = f"Request error for device {device_id}: {str(e)}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error processing device {device_id}: {str(e)}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
        
        # Prepare response
        response_data = {
            "message": "Collar API sync completed",
            "total_devices": len(device_locations),
            "sent": sent_count,
            "errors": len(errors)
        }
        
        if errors:
            response_data["error_details"] = errors
        
        print(f"Collar API sync completed: {sent_count} sent, {len(errors)} errors")
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Unexpected error in sync_to_collar_api: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
