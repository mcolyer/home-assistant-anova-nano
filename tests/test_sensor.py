"""Test sensor for simple integration."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.anova_nano.const import DOMAIN
from custom_components.anova_nano.coordinator import AnovaNanoDataUpdateCoordinator

from .const import MOCK_CONFIG


async def test_sensor(hass, bypass_get_data):
    """Test sensor."""
    bypass_get_data("custom_components.anova_nano.coordinator")

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    coordinator: AnovaNanoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_refresh()

    for sensor in [
        "water_temperature",
        "heater_temperature",
        "triac_temperature",
        "internal_temperature",
        "motor_speed",
    ]:
        entity_name = f"sensor.anova_nano_{sensor}"
        state = hass.states.get(entity_name)
        assert state, f"Got no state for: {entity_name}"

        if sensor == "water_temperature":
            # TODO: Why is the state a str?
            assert state.state == "42.0"
