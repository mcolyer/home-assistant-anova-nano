# Anova Nano Home Asssistant Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

_Integration to Anova Nano sous vide cooker for Home Assistant_

![Screenshot of Anova Nano Integration](https://private-user-images.githubusercontent.com/8842084/371416317-f72d967c-e161-43a1-9f47-164f2cbc7c51.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mjc4MzY0ODEsIm5iZiI6MTcyNzgzNjE4MSwicGF0aCI6Ii84ODQyMDg0LzM3MTQxNjMxNy1mNzJkOTY3Yy1lMTYxLTQzYTEtOWY0Ny0xNjRmMmNiYzdjNTEucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MTAwMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDEwMDJUMDIyOTQxWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZTM4ZGQzMGVjYTE1ZTBiYjEwODlhN2I4ZjIzMDQwZDhmYTA1YTVkZmRiNWRlMmFjNTVjYjBkNTZkYmMzOWQwNCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.zS0TWOgelZXubzhvfpup3Q5mdpP5GrN_ITiyT2j3f9s)

**Warning: This integration doesn't work with ESPHome Bluetooth proxies currently.**

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `anova_nano`.
1. Download _all_ the files from the `custom_components/anova_nano/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Anova Nano"

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

[pyanova_nano]: https://github.com/filmkorn/pyanova-nano
[commits-shield]: https://img.shields.io/github/commit-activity/y/mcolyer/hacs-anova-nano.svg?style=for-the-badge
[commits]: https://github.com/mcolyer/hacs-anova-nano/commits/main
[license-shield]: https://img.shields.io/github/license/mcolyer/hacs-anova-nano.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Matt%20Colyer%20%40mcolyer-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/mcolyer/hacs-anova-nano.svg?style=for-the-badge
[releases]: https://github.com/mcolyer/hacs-anova-nano/releases
