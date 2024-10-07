"""Tests for Anova Nano integration."""

from unittest.mock import patch


def patch_async_setup_entry(return_value=True):
    """Patch async setup entry to return True."""
    return patch(
        "custom_components.anova_nano.async_setup_entry",
        return_value=return_value,
    )
