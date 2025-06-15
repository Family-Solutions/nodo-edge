from datetime import datetime
from location.domain.entities.location_record import LocationRecord
from location.infrastructure.repositories.location_repository import LocationRecordRepository
from iam.infrastructure.repositories import DeviceRepository

class LocationRecordApplicationService:
    def __init__(self):
        self.repo = LocationRecordRepository()
        self.device_repo = DeviceRepository()

    def create_location_record(self, device_id: str, lat: float, lon: float, created_at: str, api_key: str) -> LocationRecord:
        if not self.device_repo.find_by_id_and_api_key(device_id, api_key):
            raise ValueError("Device not found")
        record = LocationRecord(device_id, lat, lon, datetime.fromisoformat(created_at))
        return self.repo.save(record)
