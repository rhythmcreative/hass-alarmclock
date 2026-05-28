"""Select platform for Alarm Clock integration."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NAME_REPEAT

REPEAT_OPTIONS = {
    "none": "Solo una vez",
    "daily": "Diario",
    "weekdays": "Entre semana (L-V)",
    "weekends": "Fines de semana (S-D)"
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Alarm Clock select platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    device = data["device"]
    
    async_add_entities([AlarmRepeatSelect(device)])

class AlarmRepeatSelect(SelectEntity):
    """Select entity for the alarm repeat pattern."""

    def __init__(self, device) -> None:
        """Initialize the select entity."""
        self._device = device
        self._attr_name = f"{device.name} {NAME_REPEAT}"
        self._attr_unique_id = f"{device.entry_id}_repeat"
        self._attr_device_info = device.device_info
        self._attr_options = list(REPEAT_OPTIONS.values())

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the current state."""
        repeat = self._device.repeat
        if repeat is None: return REPEAT_OPTIONS["none"]
        if repeat == "daily": return REPEAT_OPTIONS["daily"]
        if repeat == [0, 1, 2, 3, 4]: return REPEAT_OPTIONS["weekdays"]
        if repeat == [5, 6]: return REPEAT_OPTIONS["weekends"]
        return REPEAT_OPTIONS["none"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        pattern = None
        for key, value in REPEAT_OPTIONS.items():
            if value == option:
                if key == "daily": pattern = "daily"
                elif key == "weekdays": pattern = [0, 1, 2, 3, 4]
                elif key == "weekends": pattern = [5, 6]
                break
        
        await self._device.async_set_repeat(pattern)
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register update callback."""
        self._device.register_update_callback(self.async_write_ha_state)
