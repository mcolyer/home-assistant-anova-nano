"""Number platform for Anova Nano."""
import asyncio
from dataclasses import dataclass

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import AnovaNanoDataUpdateCoordinator
from .const import DOMAIN
from .entity import AnovaNanoDescriptionEntity


@dataclass(kw_only=True)
class AnovaNanoNumberEntityDescription(NumberEntityDescription):
    """Describes Anova Nano number entity."""

    set_fn: str
    state_attr: str


ENTITY_DESCRIPTIONS = [
    AnovaNanoNumberEntityDescription(
        key="cooking_timer",
        name="Cooking Timer",
        icon="mdi:timer-cog-outline",
        translation_key="cooking_time",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        device_class=NumberDeviceClass.DURATION,
        set_fn="set_timer",
        state_attr="timer",
    ),
    AnovaNanoNumberEntityDescription(
        key="target_temp",
        name="Target Temperature",
        icon="mdi:water-thermometer-outline",
        translation_key="target_temp",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=NumberDeviceClass.TEMPERATURE,
        native_max_value=92,
        native_min_value=0,
        native_step=0.1,
        set_fn="set_target_temperature",
        state_attr="target_temperature",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Set up the binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        AnovaNanoNumberEntity(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AnovaNanoNumberEntity(AnovaNanoDescriptionEntity, NumberEntity):
    """Representation of an Anova Nano number entity."""

    def __init__(
        self,
        coordinator: AnovaNanoDataUpdateCoordinator,
        entity_description: AnovaNanoNumberEntityDescription,
    ):
        """Initialize the number entity."""
        super().__init__(coordinator, description=entity_description)
        self.entity_description: AnovaNanoNumberEntityDescription = entity_description

    @property
    def native_value(self):
        """Return the current value of the number entity."""
        return getattr(self.coordinator, self.entity_description.state_attr)

    async def async_set_native_value(self, value: float):
        """Set the value of the number entity."""
        func = getattr(self.coordinator, self.entity_description.set_fn)

        await func(value)

        # TODO: Check thread safety in pyanova_nano.
        await asyncio.sleep(0.1)

        await self.coordinator.async_request_refresh()
