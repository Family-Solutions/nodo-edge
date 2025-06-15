from location.domain.entities.location_record import LocationRecord
from location.infrastructure.models.location_record import LocationRecord as LocationRecordModel

class LocationRecordRepository:
    @staticmethod
    def save(record: LocationRecord) -> LocationRecord:
        db_record = LocationRecordModel.create(
            device_id=record.device_id,
            latitude=record.latitude,
            longitude=record.longitude,
            created_at=record.created_at
        )
        return LocationRecord(
            db_record.device_id,
            db_record.latitude,
            db_record.longitude,
            db_record.created_at,
            db_record.id
        )
