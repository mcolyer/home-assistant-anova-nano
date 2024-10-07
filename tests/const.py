"""Constants for Anova Nano tests."""

from bleak import AdvertisementData, BLEDevice
from habluetooth import BluetoothServiceInfoBleak
from homeassistant.const import CONF_ADDRESS

_SERVICE_UUID = "0e140000-0af1-4582-a242-773e63054c68"
_NAME = None
_ADDRESS = "AA:BB:CC:DD:EE:FF"
_MANUFACTURER_DATA = {}

# Data stored in hass config after successful config flow.
MOCK_CONFIG = {CONF_ADDRESS: _ADDRESS}


def generate_mock_service_info(address: str) -> BluetoothServiceInfoBleak:
    """Generate a mock BluetoothServiceInfoBleak object for testing."""
    return BluetoothServiceInfoBleak(
        name=_NAME,
        manufacturer_data=_MANUFACTURER_DATA,
        service_data={},
        service_uuids=[_SERVICE_UUID],
        address=address,
        rssi=-123,
        source="local",
        advertisement=AdvertisementData(
            local_name=_NAME,
            manufacturer_data=_MANUFACTURER_DATA,
            service_data={},
            service_uuids=[_SERVICE_UUID],
            # Defaults from:
            # homeassistant.core.tests.components.bluetooth.ADVERTISEMENT_DATA_DEFAULTS
            platform_data=((),),
            rssi=-127,
            tx_power=-127,
        ),
        # Defaults from:
        # homeassistant.core.tests.components.bluetooth.BLE_DEVICE_DEFAULTS
        device=BLEDevice(address, "Nano", details=None, rssi=-127),
        time=0,
        connectable=True,
        tx_power=-127,
    )


MOCK_SERVICE_INFO = generate_mock_service_info(_ADDRESS)
