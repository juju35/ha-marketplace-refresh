"""Sensors: status of the check with its progress, and the time of the last check."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, ClassVar

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MarketplaceRefreshConfigEntry
from .const import STATE_ERROR, STATE_IDLE, STATE_RUNNING
from .entity import MarketplaceRefreshEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: MarketplaceRefreshConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities(
        [
            StatusSensor(entry.runtime_data, entry.entry_id, "status"),
            LastCheckSensor(entry.runtime_data, entry.entry_id, "last_check"),
        ]
    )


class StatusSensor(MarketplaceRefreshEntity, SensorEntity):
    """idle / running / error, with the progress as attributes."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options: ClassVar[list[str]] = [STATE_IDLE, STATE_RUNNING, STATE_ERROR]
    # Lists that change at every repository checked or installed: kept out of the recorder.
    _unrecorded_attributes = frozenset({"failed", "not_checked", "checking", "installing", "install_failed"})

    @property
    def native_value(self) -> str:
        return self.refresher.state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        r = self.refresher
        return {
            "done": r.done,
            "total": r.total,
            "updates": r.updates,
            "failed": list(r.failed),
            "not_checked": list(r.not_checked),
            "error": r.error,
            "checking": sorted(r.checking),
            "installing": list(r.installing),
            "install_failed": list(r.install_failed),
            "github_connected": r.github_connected,
        }


class LastCheckSensor(MarketplaceRefreshEntity, SensorEntity):
    """End of the last check, scheduled or manual."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> datetime | None:
        return self.refresher.last_check

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """The automatic check's interval (hours, 0 = off) and when it is due, for the card."""
        r = self.refresher
        hours = r.scan_interval
        # As set by the scheduler (an hour after a failed check); before it starts, one interval after the last check.
        last = r.last_check or r.since
        due = (r.next_due or (last + timedelta(hours=hours) if last else None)) if hours > 0 else None
        return {"scan_interval": hours, "next_check": due.isoformat() if due else None}
