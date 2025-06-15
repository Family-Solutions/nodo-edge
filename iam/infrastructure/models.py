"""Peewee models for the IAM bounded context."""
from peewee import Model, CharField, DateTimeField
from shared.infrastructure.database import db


class Device(Model):
    """Peewee model for the 'devices' table.

    Attributes:
        device_id (CharField): Unique identifier (primary key).
        api_key (CharField): API key for authentication.
        created_at (DateTimeField): Creation timestamp.
    """
    device_id   = CharField(primary_key=True)
    api_key     = CharField()
    created_at  = DateTimeField()

    class Meta:
        """Metadata for the Device model."""
        database    = db
        table_name  = 'devices'
