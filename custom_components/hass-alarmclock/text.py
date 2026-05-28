"""Text platform for Alarm Clock integration."""
from __future__ import annotations

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_NAME

from .const import DOMAIN, NAME_ALARM_SOUND

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Alarm Clock text platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    device = data["device"]
    
    async_add_entities([AlarmSoundText(device)])

class AlarmSoundText(TextEntity):
    """Text entity for the alarm sound."""

    def __init__(self, device) -> None:
        """Initialize the text entity."""
        self._device = device
        self._attr_name = f"{device.name} {NAME_ALARM_SOUND}"
        self._attr_unique_id = f"{device.entry_id}_alarm_sound"
        self._attr_device_info = device.device_info
        self._attr_native_value = device.alarm_sound

    @property
    def native_value(self) -> str | None:
        """Return the value reported by the text."""
        return self._device.alarm_sound

    async def async_set_value(self, value: str) -> None:
        """Change the value."""
        await self._device.async_set_alarm_sound(value)
        self.async_write_had_update()

    def async_write_had_update(self) -> None:
        """Update the entity."""
        self._attr_native_value = self._device.alarm_sound
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register update callback."""
        self._device.register_update_callback(self.async_write_had_update)
