"""Intents for the Alarm Clock integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent, config_validation as cv

from .const import DOMAIN

INTENT_SET_ALARM = "HassAlarmClockSet"

async def async_setup_intents(hass: HomeAssistant) -> None:
    """Set up intents."""
    intent.async_register(hass, SetAlarmIntent())

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

        # Try to find the entity_id for this alarm name
        # We assume the user might say "the bedroom alarm"
        entity_id = f"switch.{name.lower().replace(' ', '_')}_{name.lower().replace(' ', '_')}"
        
        # Call the service
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
