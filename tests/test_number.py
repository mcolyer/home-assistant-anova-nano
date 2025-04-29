"""Test the Anova Nano number platform."""

from unittest.mock import AsyncMock, patch
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.components.number import NumberDeviceClass
from custom_components.anova_nano.number import (
    AnovaNanoNumberEntity,
    AnovaNanoTargetTempNumberEntity,
    ENTITY_DESCRIPTIONS,
)
from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.anova_nano.const import DOMAIN
from .const import MOCK_CONFIG
from homeassistant.const import CONF_ADDRESS


@pytest.fixture
def mock_coordinator(hass):
    """Create a mock coordinator."""
    coordinator = AsyncMock()
    coordinator.address = MOCK_CONFIG[CONF_ADDRESS]
    coordinator.status = AsyncMock()
    coordinator.status.water_temp_units = "C"
    coordinator.timer = 30
    coordinator.set_timer = AsyncMock()
    coordinator.target_temperature = 60.0
    coordinator.temp_units = UnitOfTemperature.CELSIUS
    return coordinator


async def test_number_entity_native_value(hass, mock_coordinator):
    """Test the native_value property of number entities."""
    for description in ENTITY_DESCRIPTIONS:
        entity = AnovaNanoNumberEntity(mock_coordinator, description)
        assert entity.native_value == getattr(mock_coordinator, description.state_attr)


async def test_number_entity_set_native_value(hass, mock_coordinator):
    """Test setting the native value of number entities."""
    for description in ENTITY_DESCRIPTIONS:
        entity = AnovaNanoNumberEntity(mock_coordinator, description)
        new_value = 45.0 if description.key == "target_temp" else 45
        await entity.async_set_native_value(new_value)
        set_fn = getattr(mock_coordinator, description.set_fn)
        set_fn.assert_called_once_with(new_value)
        mock_coordinator.async_request_refresh.assert_called_once()
        mock_coordinator.async_request_refresh.reset_mock()


async def test_number_entity_native_unit_of_measurement(hass, mock_coordinator):
    """Test the native_unit_of_measurement property of number entities."""
    for description in ENTITY_DESCRIPTIONS:
        if "target_temp" in description.key:
            entity = AnovaNanoTargetTempNumberEntity(mock_coordinator, description)
            mock_coordinator.temp_units = UnitOfTemperature.CELSIUS
            assert entity.native_unit_of_measurement == UnitOfTemperature.CELSIUS
            assert entity.native_max_value == 92
            mock_coordinator.temp_units = UnitOfTemperature.FAHRENHEIT
            assert entity.native_unit_of_measurement == UnitOfTemperature.FAHRENHEIT
            assert entity.native_min_value == 32
            assert entity.native_max_value == 197
        else:
            entity = AnovaNanoNumberEntity(mock_coordinator, description)
            assert entity.native_unit_of_measurement == UnitOfTime.MINUTES


async def test_target_temp_unit_of_measurement_converted(
    hass, mock_coordinator, monkeypatch
):
    """Ensure units are converted from units set in configuration to units set on device."""
    target_temp_entity_description = ENTITY_DESCRIPTIONS[1]
    entity = AnovaNanoTargetTempNumberEntity(
        mock_coordinator, target_temp_entity_description
    )
    assert entity.native_unit_of_measurement == UnitOfTemperature.CELSIUS
    monkeypatch.setattr(entity, "hass", hass)

    # Device set to Celsius, hass set to Fahrenheit.
    hass.config.units.temperature_unit = UnitOfTemperature.FAHRENHEIT
    mock_coordinator.temp_units = UnitOfTemperature.CELSIUS
    assert entity.native_value == 60.0
    assert entity.value == 140.0

    # Device set to Fahrenheit, hass set to Celsius
    mock_coordinator.temp_units = UnitOfTemperature.FAHRENHEIT
    hass.config.units.temperature_unit = UnitOfTemperature.CELSIUS
    assert entity.native_value == 60.0
    assert round(float(entity.value or 0.0), 1) == 15.6

    # Both device and hass set to Celsius.
    hass.config.units.temperature_unit = UnitOfTemperature.CELSIUS
    mock_coordinator.temp_units = UnitOfTemperature.CELSIUS
    assert entity.value == 60.0
    assert entity.native_value == 60.0


async def test_async_setup_entry(hass: HomeAssistant, mock_coordinator):
    """Test the async_setup_entry function."""
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    for number in ["cooking_timer", "target_temperature"]:
        entity_id = f"number.anova_nano_{number}"
        assert entity_id in hass.states.async_entity_ids()


def test_entity_descriptions():
    """Test the entity descriptions."""
    assert len(ENTITY_DESCRIPTIONS) == 2

    timer_description = ENTITY_DESCRIPTIONS[0]
    assert timer_description.key == "cooking_timer"
    assert timer_description.name == "Cooking Timer"
    assert timer_description.icon == "mdi:timer-cog-outline"
    assert timer_description.translation_key == "cooking_time"
    assert timer_description.native_unit_of_measurement == UnitOfTime.MINUTES
    assert timer_description.device_class == NumberDeviceClass.DURATION
    assert timer_description.set_fn == "set_timer"
    assert timer_description.state_attr == "timer"

    temp_description = ENTITY_DESCRIPTIONS[1]
    assert temp_description.key == "target_temp"
    assert temp_description.name == "Target Temperature"
    assert temp_description.icon == "mdi:water-thermometer-outline"
    assert temp_description.translation_key == "target_temp"
    assert temp_description.device_class == NumberDeviceClass.TEMPERATURE
    assert temp_description.native_step == 0.1
    assert temp_description.set_fn == "set_target_temperature"
    assert temp_description.state_attr == "target_temperature"


async def test_number_entity_set_native_value_with_sleep(hass, mock_coordinator):
    """Test setting the native value of number entities with sleep."""
    for description in ENTITY_DESCRIPTIONS:
        entity = AnovaNanoTargetTempNumberEntity(mock_coordinator, description)
        new_value = 45.0 if description.key == "target_temp" else 45
        with patch("asyncio.sleep") as mock_sleep:
            await entity.async_set_native_value(new_value)
            set_fn = getattr(mock_coordinator, description.set_fn)
            set_fn.assert_called_once_with(new_value)
            mock_sleep.assert_called_once_with(0.1)
            mock_coordinator.async_request_refresh.assert_called_once()
            mock_coordinator.async_request_refresh.reset_mock()
