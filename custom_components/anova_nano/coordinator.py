"""DataUpdateCoordinator for anova_nano."""
from __future__ import annotations

import asyncio
import logging
from asyncio import timeout
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.components import bluetooth
from habluetooth import BluetoothServiceInfoBleak
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyanova_nano import PyAnova

from .const import DOMAIN, TIMEOUT, UPDATE_INTERVAL

if TYPE_CHECKING:
    from pyanova_nano.types import SensorValues

DEVICE_STARTUP_TIMEOUT = 60


class AnovaNanoDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching example data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        entry: ConfigEntry,
    ) -> None:
        """Initialize example data coordinator."""
        super().__init__(
            hass=hass,
            logger=logger,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.config_entry: ConfigEntry = entry
        self._hass: HomeAssistant = hass
        self._address: str = entry.data[CONF_ADDRESS]

        self._client: PyAnova | None = None

        self.status: SensorValues | None = None
        self.timer: int | None = None
        self.target_temperature: float | None = None

    async def _connect(self):
        """Ensure the client is connected."""
        if self._client and self._client.is_connected():
            return

        if not self._client:
            ble_device = bluetooth.async_ble_device_from_address(
                self._hass, address=self._address.upper(), connectable=True
            )
            if not ble_device:
                raise UpdateFailed(
                    f"Could not discover a {self.name} with address: {self._address}"
                )

            self._client = PyAnova(self._hass.loop, device=ble_device)

        try:
            await self._client.connect()
        except TimeoutError as err:
            self._client = None
            raise UpdateFailed(
                f"Unable to connect to {self.name} with address: {self._address}"
            ) from err

    async def disconnect(self):
        await self._client.disconnect()
        self._client = None

    @property
    def client(self) -> PyAnova:
        """The API client."""
        return self._client

    async def _async_update_data(
        self, service_info: BluetoothServiceInfoBleak = None
    ) -> SensorValues:
        """Update the device status."""
        await self._connect()

        async with timeout(TIMEOUT):
            try:
                self.status = await self.client.get_sensor_values()
                self.timer = await self.client.get_timer()
                self.target_temperature = await self.client.get_target_temperature()
            except Exception as err:
                raise UpdateFailed(err) from err

        return self.status

    async def turn_on(self):
        """Start cooking."""
        await self._connect()

        try:
            await self.client.start()
        except Exception as err:  # TODO: Narrow down
            raise UpdateFailed(err) from err

        # Wait for the motor to spin up.
        await asyncio.sleep(1.0)

    async def turn_off(self):
        """Stop cooking."""
        await self._connect()

        try:
            await self.client.stop()
        except Exception as err:  # TODO: Narrow down
            raise UpdateFailed(err) from err

    async def set_timer(self, minutes: int):
        await self._connect()

        try:
            await self.client.set_timer(int(minutes))
        except Exception as err:  # TODO: Narrow down
            raise UpdateFailed(err) from err

        self.timer = minutes

    async def set_target_temperature(self, temp: float):
        await self._connect()

        try:
            await self.client.set_target_temperature(temp)
        except Exception as err:  # TODO: Narrow down
            raise UpdateFailed(err) from err

        self.target_temperature = temp
