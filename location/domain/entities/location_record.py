from datetime import datetime

class LocationRecord:
    def __init__(self, device_id: str, latitude: float, longitude: float, created_at: datetime, id: int = None):
        self.id = id
        self.device_id = device_id
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = created_at
