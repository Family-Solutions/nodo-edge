from datetime import datetime
from location.domain.entities.location_record import LocationRecord
from location.infrastructure.repositories.location_repository import LocationRecordRepository

class LocationRecordApplicationService:
    def __init__(self):
        self.repo = LocationRecordRepository()

    def create_location_record(self, device_id: str, lat: float, lon: float, created_at: str) -> LocationRecord:
        record = LocationRecord(device_id, lat, lon, datetime.fromisoformat(created_at))
        return self.repo.save(record)

    def get_all_location_records(self) -> list[LocationRecord]:
        """Get all location records."""
        return self.repo.find_all()

    def find_by_device_id(self, device_id: str) -> LocationRecord:
        """Find a location record by device_id."""
        return self.repo.find_by_device_id(device_id)
    
    def update_location_record(self, device_id: str, lat: float, lon: float, created_at: str) -> LocationRecord:
        """Update an existing location record."""
        record = LocationRecord(device_id, lat, lon, datetime.fromisoformat(created_at))
        return self.repo.update_by_device_id(device_id, record)
