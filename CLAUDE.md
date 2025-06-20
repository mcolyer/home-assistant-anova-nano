# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant custom integration for the Anova Nano sous vide cooker. It uses Bluetooth Low Energy (BLE) to communicate with the device via the `pyanova-nano` library.

## Architecture

- **Integration Entry Point**: `custom_components/anova_nano/__init__.py` - Sets up platforms and Bluetooth callbacks
- **Data Coordinator**: `custom_components/anova_nano/coordinator.py` - Manages BLE communication and data updates using `pyanova-nano`
- **Platform Files**: Separate files for each Home Assistant platform (sensor, binary_sensor, switch, number)
- **Config Flow**: `config_flow.py` - Handles device discovery and configuration via Bluetooth
- **Entity Base**: `entity.py` - Base entity class for all Anova Nano entities

The integration uses Home Assistant's DataUpdateCoordinator pattern for managing device state and updates. All communication with the Anova Nano device is handled through the coordinator using the `pyanova-nano` library.

## Development Commands

**Setup environment:**
```bash
scripts/setup  # Installs uv and creates virtual environment
```

**Development server (with Home Assistant):**
```bash
scripts/develop  # Runs local Home Assistant instance with integration loaded
```

**Testing:**
```bash
scripts/test  # Runs pytest test suite
```

**Code quality:**
```bash
scripts/lint    # Runs ruff linter with auto-fix
scripts/format  # Runs black formatter
```

## Testing

- Uses pytest with `pytest-homeassistant-custom-component`
- Test files are in `tests/` directory
- Run individual tests: `pytest tests/test_sensor.py`
- Tests use Home Assistant's testing framework and fixtures

## Dependencies

- **Runtime**: `pyanova-nano` library for device communication, Home Assistant core
- **Development**: ruff for linting, black for formatting, pytest for testing
- **Python**: Requires Python 3.12+
- **Environment**: Uses `uv` for dependency management

## Bluetooth Integration

The integration relies on Home Assistant's Bluetooth component and registers callbacks for device discovery. The device uses service UUID `0e140000-0af1-4582-a242-773e63054c68` for BLE communication.