"""DataUpdateCoordinator for anova_nano."""
from __future__ import annotations

import asyncio
import logging
from asyncio import timeout
from datetime import timedelta
from typing import TYPE_CHECKING, Optional

from habluetooth import BluetoothServiceInfoBleak
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyanova_nano import PyAnova

from .const import DOMAIN, UPDATE_INTERVAL, TIMEOUT

if TYPE_CHECKING:
    from bleak.backends.device import BLEDevice
    from pyanova_nano.types import SensorValues

DEVICE_STARTUP_TIMEOUT = 60


class AnovaNanoDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching example data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        entry: ConfigEntry,
        client: PyAnova,
    ) -> None:
        """Initialize example data coordinator."""
        super().__init__(
            hass=hass,
            logger=logger,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.config_entry: ConfigEntry = entry
        self.client: PyAnova = client
        self.status: Optional[SensorValues] = None

    async def _async_update_data(
        self, service_info: BluetoothServiceInfoBleak = None
    ) -> SensorValues:
        """Poll the device."""
        self.logger.debug("_async_update")

        assert self.client.is_connected(), "Client is not connected!"
        async with timeout(TIMEOUT):
            try:
                self.status: SensorValues = await self.client.get_sensor_values()
            except Exception as err:
                raise UpdateFailed(err) from err

        return self.status

    async def turn_on(self):
        async with timeout(TIMEOUT):
            try:
                await self.client.start()
            except Exception as err:  # TODO: Narrow down
                raise UpdateFailed(err) from err
        # Wait for the motor to spin up.
        await asyncio.sleep(1.0)

    async def turn_off(self):
        async with timeout(TIMEOUT):
            try:
                await self.client.stop()
            except Exception as err:  # TODO: Narrow down
                raise UpdateFailed(err) from err

