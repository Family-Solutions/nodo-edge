"""Application services for the IAM bounded context."""
from typing import Optional

from iam.domain.entities import Device
from iam.domain.services import AuthService
from iam.infrastructure.repositories import DeviceRepository

class AuthApplicationService:
    """Application service for device authentication."""

    def __init__(self):
        """Initialize the AuthApplicationService."""
        self.device_repository = DeviceRepository()
        self.auth_service = AuthService()

    def authenticate(self, device_id: str, api_key: str) -> bool:
        """Authenticate a device.

        Args:
            device_id (str): Unique identifier of the device.
            api_key (str): API key for authentication.

        Returns:
            bool: True if authentication succeeds, False otherwise.
        """
        device: Optional[Device] = self.device_repository.find_by_id_and_api_key(device_id, api_key)
        return self.auth_service.authenticate(device)

    def get_or_create_test_device(self) -> Device:
        """Get or create a test device for development.

        Returns:
            Device: The test device entity.
        """
        return self.device_repository.get_or_create_test_device()