"""Constants for anova_nano."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Anova Nano BLE integration"
DOMAIN = "anova_nano"
VERSION = "0.0.0"
ATTRIBUTION = ""

SERVICE_UUID = "0e140000-0af1-4582-a242-773e63054c68"
UPDATE_INTERVAL = 60
TIMEOUT = 30
