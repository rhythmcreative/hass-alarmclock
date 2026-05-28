# Alarm Clock Enhanced (Alexa-like)

This enhanced version of the Alarm Clock integration adds Alexa-like features, custom sounds, and LLM/Assist integration.

## Features
- **Alexa-like commands**: Use Home Assistant Assist (and LLM) to set alarms by voice or text.
- **Custom Alarm Sounds**: Set a specific sound file for each alarm.
- **Dynamic Sounds**: Sounds are stored in the sensor attributes, allowing automations to play the correct file.
- **LLM Ready**: Exposes intents that can be used by OpenAI/Ollama conversation agents in Home Assistant.

## How to use LLM commands
1. Ensure you have an LLM conversation agent (like Ollama or OpenAI) set up in Home Assistant.
2. In the Assist settings, make sure the LLM is selected.
3. You can say:
   - "Set the bedroom alarm for 7 in the morning"
   - "Put the kitchen alarm at 8pm with sound birds.mp3"

## Services
The `alarm_clock.set_alarm` service now accepts an optional `sound` field.

## Blueprint
The included blueprint `ring-alarm.yml` has been updated to automatically use the custom sound set for the alarm.

## Lovelace UI Card
I have included a custom Lovelace card to give you an Alexa-like interface at the bottom of your dashboard.

### 1. Register the Resource
Go to **Settings > Dashboards > Resources** and add:
- **URL:** `/alarm-clock-ui/alarm-clock-card.js`
- **Type:** JavaScript Module

### 2. Add the Card
Add a "Manual" card to your dashboard and use this YAML:
```yaml
type: custom:alarm-clock-card
entity: switch.bedroom_bedroom  # Change to your alarm switch
status_entity: sensor.bedroom_status
time_entity: datetime.bedroom_time
```

The card will show the time big, the status, and pulse red when the alarm is ringing, with "SNOOZE" and "STOP" buttons.
