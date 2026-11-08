"""Diagnostics for Marketplace Refresh: the entry, the last check and the Marketplace it reads."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import refresher as refresher_module
from .refresher import MarketplaceRefresher

# Nothing of the kind is stored today; redacted anyway so that a future option can't leak.
TO_REDACT = {
    "access_token",
    "api_key",
    "email",
    "github_token",
    "password",
    "refresh_token",
    "token",
    "url",
    "username",
}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """The entry's data and options, the refresher's state and what the Marketplace says about itself."""
    refresher: MarketplaceRefresher = entry.runtime_data
    marketplace = refresher_module._loaded_marketplace(hass)  # noqa: SLF001 - same module, patched in tests
    system = getattr(marketplace, "system", None)
    repositories = getattr(marketplace, "repositories", None)
    return async_redact_data(
        {
            "entry": {"data": dict(entry.data), "options": dict(entry.options)},
            "refresher": {
                "state": refresher.state,
                "done": refresher.done,
                "total": refresher.total,
                "updates": refresher.updates,
                "pending": refresher.pending,
                "failed": list(refresher.failed),
                "not_checked": list(refresher.not_checked),
                "error": refresher.error,
                "checking": sorted(refresher.checking),
                "installing": list(refresher.installing),
                "install_failed": list(refresher.install_failed),
                "github_connected": refresher.github_connected,
                "last_check": refresher.last_check.isoformat() if refresher.last_check else None,
                "next_due": refresher.next_due.isoformat() if refresher.next_due else None,
                "since": refresher.since.isoformat() if refresher.since else None,
            },
            "marketplace": {
                "loaded": marketplace is not None,
                "github_connected": getattr(marketplace, "github_connected", None),
                "disabled": getattr(system, "disabled", None),
                "disabled_reason": str(reason) if (reason := getattr(system, "disabled_reason", None)) else None,
                "installed": len(getattr(repositories, "list_installed", None) or []),
            },
        },
        TO_REDACT,
    )
