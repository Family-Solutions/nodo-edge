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

    @staticmethod
    def find_all() -> list[LocationRecord]:
        """Get all location records from the database."""
        db_records = LocationRecordModel.select()
        return [
            LocationRecord(
                record.device_id,
                record.latitude,
                record.longitude,
                record.created_at,
                record.id
            )
            for record in db_records
        ]

    @staticmethod
    def find_by_device_id(device_id: str) -> LocationRecord:
        """Find a location record by device_id."""
        try:
            db_record = LocationRecordModel.get(LocationRecordModel.device_id == device_id)
            return LocationRecord(
                db_record.device_id,
                db_record.latitude,
                db_record.longitude,
                db_record.created_at,
                db_record.id
            )
        except LocationRecordModel.DoesNotExist:
            return None

    @staticmethod
    def update_by_device_id(device_id: str, record: LocationRecord) -> LocationRecord:
        """Update a location record by device_id."""
        try:
            # Update the existing record
            query = LocationRecordModel.update(
                latitude=record.latitude,
                longitude=record.longitude,
                created_at=record.created_at
            ).where(LocationRecordModel.device_id == device_id)
            query.execute()
            
            # Return the updated record
            db_record = LocationRecordModel.get(LocationRecordModel.device_id == device_id)
            return LocationRecord(
                db_record.device_id,
                db_record.latitude,
                db_record.longitude,
                db_record.created_at,
                db_record.id
            )
        except LocationRecordModel.DoesNotExist:
            # If record doesn't exist, create it
            return LocationRecordRepository.save(record)
