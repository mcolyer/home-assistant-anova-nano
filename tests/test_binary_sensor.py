"""Test binary sensor for Anova Nano."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.anova_nano.const import DOMAIN
from custom_components.anova_nano.coordinator import AnovaNanoDataUpdateCoordinator

from .const import MOCK_CONFIG


async def test_binary_sensor(hass, bypass_get_data):
    """Test sensor."""
    bypass_get_data("custom_components.anova_nano.coordinator")

    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    coordinator: AnovaNanoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_refresh()

    for binary_sensor in ["water_low", "water_leak"]:
        state = hass.states.get(f"binary_sensor.anova_nano_{binary_sensor}")
        assert state.state == "off"
