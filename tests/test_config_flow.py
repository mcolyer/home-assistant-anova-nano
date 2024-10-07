"""Test anova_nano config flow."""
from unittest.mock import patch

import pytest
from homeassistant import config_entries, data_entry_flow
from homeassistant.config_entries import SOURCE_BLUETOOTH
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResultType

from custom_components.anova_nano.const import DOMAIN

from .const import MOCK_CONFIG, MOCK_SERVICE_INFO, generate_mock_service_info


# This fixture bypasses the actual setup of the integration
# since we only want to test the config flow. We test the
# actual functionality of the integration in other test modules.
@pytest.fixture()
def bypass_setup():
    """Prevent setup."""
    with patch(
        "custom_components.anova_nano.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry


# Here we simulate a successful config flow from the backend.
# Note that we use the `bypass_get_data` fixture here because
# we want the config flow validation to succeed during the test.
async def test_successful_config_flow(hass, bypass_setup):
    """Test discovery via bluetooth with a valid device."""
    with patch(
        "custom_components.anova_nano.config_flow.async_discovered_service_info",
        return_value=[MOCK_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_BLUETOOTH},
            data=[MOCK_SERVICE_INFO],
        )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "confirm"

    # The entry setup is bypassed using the bypass_setup fixture.
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {},
    )
    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == MOCK_SERVICE_INFO.address
    assert result["data"] == MOCK_CONFIG

    assert len(bypass_setup.mock_calls) == 1


async def test_config_flow_multiple_devices(hass, bypass_setup):
    """Test a failed config flow due to credential validation failure."""
    other_address = "VV:WW:XX:YY:ZZ"

    mock_service_info_2 = generate_mock_service_info(address=other_address)

    # When multiple devices are discovered.
    with patch(
        "custom_components.anova_nano.config_flow.async_discovered_service_info",
        return_value=[MOCK_SERVICE_INFO, mock_service_info_2],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    # The entry setup is bypassed using the bypass_setup fixture.
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_ADDRESS: other_address}
    )

    await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == mock_service_info_2.address
    assert result["data"] == {CONF_ADDRESS: other_address}

    assert len(bypass_setup.mock_calls) == 1


# Fault cases.


async def test_config_flow_no_devices(hass):
    """Test an aborted config flow due to not having discovered any devices."""
    # When no devices are discovered.
    with patch(
        "custom_components.anova_nano.config_flow.async_discovered_service_info",
        return_value=[],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
        )

    # Then the config flow aborts.
    assert result["type"] == FlowResultType.ABORT


# In this case, we want to simulate a failure during the config flow.
# We use the `error_on_get_data` mock instead of `bypass_get_data`
# (note the function parameters) to raise an Exception during
# validation of the input config.
async def skipped_test_failed_config_flow(hass, error_on_get_data):
    """Test a failed config flow due to a communication error with the device."""
    # When one device is discovered.
    with patch(
        "custom_components.anova_nano.config_flow.async_discovered_service_info",
        return_value=[MOCK_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
        )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "confirm"

    # And the setup of the entry fails.
    with patch(
        "custom_components.anova_nano.bluetooth.async_ble_device_from_address",
        return_value=MOCK_SERVICE_INFO.device,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "unknown"}
