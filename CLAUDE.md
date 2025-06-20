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

## Release Process

**Version files to update:**
- `pyproject.toml` - Main project version
- `custom_components/anova_nano/manifest.json` - Home Assistant integration version
- `custom_components/anova_nano/const.py` - VERSION constant

**Release commands:**
```bash
# Create and push tag
git tag v0.7.2
git push origin v0.7.2

# Create GitHub release
gh release create v0.7.2 --title "v0.7.2" --notes "Release notes here"
```

**Important**: Always ensure all three version files are synchronized before creating a release. The integration will not work properly if versions are mismatched.