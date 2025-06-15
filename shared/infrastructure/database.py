"""
Database initialization for the Smart Band Edge Service.

Sets up the SQLite database and creates required tables for devices and health records.
"""
from peewee import SqliteDatabase

# Initialize SQLite database
db = SqliteDatabase('collar-location.db')

def init_db() -> None:
    """
    Initialize the database and create tables for Device and HealthRecord models.
    """
    db.connect()
    from iam.infrastructure.models import Device
    from location.infrastructure.models.location_record import LocationRecord
    db.create_tables([Device, LocationRecord], safe=True)
    db.close()

