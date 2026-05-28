"""Intents for the Alarm Clock integration."""
from __future__ import annotations

import voluptuous as vol
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent, config_validation as cv

from .const import DOMAIN, STATE_TRIGGERED

_LOGGER = logging.getLogger(__name__)

INTENT_SET_ALARM = "HassAlarmClockSet"
INTENT_STOP_ALARM = "HassAlarmClockStop"
INTENT_SNOOZE_ALARM = "HassAlarmClockSnooze"

async def async_setup_intents(hass: HomeAssistant) -> None:
    """Set up intents."""
    intent.async_register(hass, SetAlarmIntent())
    intent.async_register(hass, StopAlarmIntent())
    intent.async_register(hass, SnoozeAlarmIntent())

class SetAlarmIntent(intent.IntentHandler):
    """Handle SetAlarm intents."""

    intent_type = INTENT_SET_ALARM
    slot_schema = {
        vol.Required("name"): cv.string,
        vol.Required("time"): cv.string,
        vol.Optional("sound"): cv.string,
    }

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        hass = intent_obj.hass
        slots = self.async_validate_slots(intent_obj.slots)
        
        name = slots["name"]["value"]
        time_str = slots["time"]["value"]
        sound = slots.get("sound", {}).get("value")

        entity_id = f"switch.{name.lower().replace(' ', '_')}_{name.lower().replace(' ', '_')}"
        
        service_data = {
            "entity_id": entity_id,
            "time": time_str,
        }
        if sound:
            service_data["sound"] = sound

        await hass.services.async_call(
            DOMAIN,
            "set_alarm",
            service_data,
            blocking=True,
        )

        response = intent_obj.create_response()
        response.async_set_speech(f"Alarma configurada para las {time_str} en {name}")
        return response

class StopAlarmIntent(intent.IntentHandler):
    """Handle StopAlarm intents."""

    intent_type = INTENT_STOP_ALARM
    slot_schema = {
        vol.Optional("name"): cv.string,
    }

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        hass = intent_obj.hass
        slots = self.async_validate_slots(intent_obj.slots)
        name = slots.get("name", {}).get("value")
        
        target_entity = None
        
        if name:
            target_entity = f"switch.{name.lower().replace(' ', '_')}_{name.lower().replace(' ', '_')}"
        else:
            # Look for ANY triggered alarm
            for entry_id, entry_data in hass.data[DOMAIN].items():
                device = entry_data["device"]
                if device.status == STATE_TRIGGERED:
                    target_entity = f"switch.{device.name.lower().replace(' ', '_')}_{device.name.lower().replace(' ', '_')}"
                    break
        
        if target_entity:
            await hass.services.async_call(
                DOMAIN,
                "stop",
                {"entity_id": target_entity},
                blocking=True,
            )
            response = intent_obj.create_response()
            response.async_set_speech("Alarma detenida.")
            return response
        
        response = intent_obj.create_response()
        response.async_set_speech("No hay ninguna alarma sonando en este momento.")
        return response

class SnoozeAlarmIntent(intent.IntentHandler):
    """Handle SnoozeAlarm intents."""

    intent_type = INTENT_SNOOZE_ALARM
    slot_schema = {
        vol.Optional("name"): cv.string,
    }

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        hass = intent_obj.hass
        slots = self.async_validate_slots(intent_obj.slots)
        name = slots.get("name", {}).get("value")
        
        target_entity = None
        
        if name:
            target_entity = f"switch.{name.lower().replace(' ', '_')}_{name.lower().replace(' ', '_')}"
        else:
            for entry_id, entry_data in hass.data[DOMAIN].items():
                device = entry_data["device"]
                if device.status == STATE_TRIGGERED:
                    target_entity = f"switch.{device.name.lower().replace(' ', '_')}_{device.name.lower().replace(' ', '_')}"
                    break
        
        if target_entity:
            await hass.services.async_call(
                DOMAIN,
                "snooze",
                {"entity_id": target_entity},
                blocking=True,
            )
            response = intent_obj.create_response()
            response.async_set_speech("Alarma pospuesta.")
            return response
        
        response = intent_obj.create_response()
        response.async_set_speech("No hay ninguna alarma para posponer.")
        return response
