"""DataUpdateCoordinator for anova_nano."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from habluetooth import BluetoothServiceInfoBleak
from homeassistant.components import bluetooth
from homeassistant.components.bluetooth.active_update_coordinator import (
    ActiveBluetoothDataUpdateCoordinator,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CoreState, HomeAssistant, callback
from pyanova_nano import PyAnova

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from bleak.backends.device import BLEDevice
    from pyanova_nano.types import SensorValues


class AnovaNanoDataUpdateCoordinator(ActiveBluetoothDataUpdateCoordinator[None]):
    """Class to manage fetching example data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        entry: ConfigEntry,
        ble_device: BLEDevice,
    ) -> None:
        """Initialize example data coordinator."""
        super().__init__(
            hass=hass,
            logger=logger,
            address=ble_device.address,
            needs_poll_method=self._needs_poll,
            poll_method=self._async_update,
            mode=bluetooth.BluetoothScanningMode.ACTIVE,
            connectable=True,
        )
        self.config_entry: ConfigEntry = entry
        self.client: PyAnova = PyAnova(loop=hass.loop, device=ble_device)

        self.status: SensorValues = None

        self.last_update_success: bool = False
        self._was_unavailable = True

    @callback
    def _needs_poll(
        self,
        service_info: bluetooth.BluetoothServiceInfoBleak,
        seconds_since_last_poll: float | None,
    ) -> bool:
        # Only poll if hass is running, we need to poll,
        # and we actually have a way to connect to the device
        if self.hass.state != CoreState.running:
            return False

        needs_poll = (
            (seconds_since_last_poll is None or seconds_since_last_poll > 60)
            and bool(
                bluetooth.async_ble_device_from_address(
                    self.hass, service_info.device.address, connectable=True
                )
            )
        )
        self.logger.debug("Needs poll %s", needs_poll)
        return needs_poll

    async def _async_update(
        self, service_info: BluetoothServiceInfoBleak
    ) -> None:
        """Poll the device."""
        try:
            self.status: SensorValues = await self.client.get_sensor_values()
        except Exception as e:
            self.logger.exception(e)
            # TODO: Narrow down exception type
            self.last_update_success = False
        else:
            self.last_update_success = True

    @callback
    def _async_handle_unavailable(
        self, service_info: BluetoothServiceInfoBleak
    ) -> None:
        """Handle the device going unavailable."""
        super()._async_handle_unavailable(service_info)
        self._was_unavailable = True

    @callback
    def _async_handle_bluetooth_event(
        self,
        service_info: BluetoothServiceInfoBleak,
        change: bluetooth.BluetoothChange,
    ) -> None:
        """Handle a Bluetooth event."""
        self.logger.debug("Bluetooth event: service info: %s", service_info)
        self.logger.debug("Bluetooth event: change: %s", change)
        self._was_unavailable = False

        super()._async_handle_bluetooth_event(service_info, change)
