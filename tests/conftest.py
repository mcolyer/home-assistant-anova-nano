"""Global fixtures for Anova Nano integration."""

from unittest.mock import patch

import pytest
from bleak import BLEDevice
from pytest_socket import enable_socket, socket_allow_hosts
from pyanova_nano.types import SensorValues


pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.hookimpl(trylast=True)
def pytest_runtest_setup():
    """Ensure the bluetooth integration we depend on can load.

    https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/issues/154#issuecomment-2065081783

    """
    enable_socket()
    socket_allow_hosts(
        # Allow "None" to allow the bluetooth integration to load.
        ["None"],
        allow_unix_socket=True,
    )


# This fixture is used to enable custom integrations, otherwise the custom_components folder will not be loaded.
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with (
        patch("homeassistant.components.persistent_notification.async_create"),
        patch("homeassistant.components.persistent_notification.async_dismiss"),
    ):
        yield


# This fixture, when used, will result in calls to async_get_data to return None. To have the call
# return a value, we would add the `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture(monkeypatch):
    """Skip calls to get data from API."""

    def mock_async_ble_from_address(hass, address, connectable):
        return BLEDevice(address=address, name="abc", rssi=-15, details=None)

    async def mock_connect(
        self, device: BLEDevice | None = None, timeout_seconds: int | None = None
    ):
        return

    async def mockget_sensor_values(self) -> SensorValues:
        return SensorValues(
            water_temp=42.0,
            water_temp_units="C",
            heater_temp=69.0,
            heater_temp_units="C",
            triac_temp=20.0,
            triac_temp_units="C",
            internal_temp=23.0,
            internal_temp_units="C",
            water_low=False,
            water_leak=False,
            motor_speed=150,
        )

    async def mock_get_target_temperature(self) -> float:
        return 42.0

    async def mock_get_timer(self) -> int:
        return 69

    async def mock_get_unit(self) -> str:
        return "C"

    def patch(module: str):
        monkeypatch.setattr(
            f"{module}.bluetooth.async_ble_device_from_address",
            mock_async_ble_from_address,
        )

        monkeypatch.setattr(
            f"{module}.PyAnova.connect",
            mock_connect,
        )
        monkeypatch.setattr(
            f"{module}.PyAnova.get_unit",
            mock_get_unit,
        )
        monkeypatch.setattr(
            f"{module}.PyAnova.get_sensor_values",
            mockget_sensor_values,
        )
        monkeypatch.setattr(
            f"{module}.PyAnova.get_target_temperature",
            mock_get_target_temperature,
        )
        monkeypatch.setattr(
            f"{module}.PyAnova.get_timer",
            mock_get_timer,
        )

    yield patch


# In this fixture, we are forcing calls to async_get_data to raise an Exception. This is useful
# for exception handling.
@pytest.fixture(name="error_on_connect")
def error_on_connect_fixture(monkeypatch):
    """Simulate error when retrieving data from API."""

    async def mock_connect_raises(self):
        raise TimeoutError

    monkeypatch.setattr(
        "custom_components.anova_nano.config_flow.PyAnova.connect",
        mock_connect_raises,
    )
    yield
