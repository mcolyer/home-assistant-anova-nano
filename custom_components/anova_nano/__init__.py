"""Custom integration to integrate Anova Nano with Home Assistant.

For more details about this integration, please refer to
https://github.com/mcolyer/hacs-anova-nano
"""
from __future__ import annotations

import logging

from pyanova_nano import PyAnova

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import AnovaNanoDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]

_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})
    connectable = True
    address: str = entry.data[CONF_ADDRESS]

    ble_device = bluetooth.async_ble_device_from_address(
        hass, address=address.upper(), connectable=connectable
    )
    if not ble_device:
        raise ConfigEntryNotReady(
            f"Could not find a Anova Nano with address: {address}"
        )

    client = PyAnova(loop=hass.loop, device=ble_device)

    try:
        await client.connect(device=ble_device)
    except TimeoutError as err:
        raise ConfigEntryNotReady(
            f"Could not connect to the Anova Nano with address: {address}"
        ) from err

    coordinator_ = hass.data[DOMAIN][entry.entry_id] = AnovaNanoDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        entry=entry,
        client=client,
    )
    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    # await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
