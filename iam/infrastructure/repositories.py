"""Repositories for the IAM bounded context."""
from typing import Optional

import peewee

from iam.domain.entities import Device
from iam.infrastructure.models import Device as DeviceModel

class DeviceRepository:
    """Repository for managing Device entities."""

    @staticmethod
    def find_by_id_and_api_key(device_id: str, api_key: str) -> Optional[Device]:
        """Find a device by its ID and API key.

        Args:
            device_id (str): Unique identifier of the device.
            api_key (str): API key for authentication.

        Returns:
            Optional[Device]: Device entity if found, None otherwise.
        """
        try:
            device = DeviceModel.get(
                (DeviceModel.device_id == device_id) & (DeviceModel.api_key == api_key)
            )
            return Device(device.device_id, device.api_key, device.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_test_device() -> Device:
        """Get or create a test device for development.

        Returns:
            Device: The test device entity.
        """
        device, _ = DeviceModel.get_or_create(
            device_id="gps-collar-001",
            defaults={"api_key": "test-api-key-123", "created_at": "2025-06-04T23:23:00Z"}
        )
        return Device(device.device_id, device.api_key, device.created_at)