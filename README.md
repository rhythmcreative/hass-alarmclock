# Home Assistant Alarm Clock Integration (Enhanced "Alexa-Style")

![Version](https://img.shields.io/badge/version-1.1.0-blue) ![Status](https://img.shields.io/badge/status-actively%20maintained-brightgreen)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A fully customizable, intelligent alarm clock integration for Home Assistant. This enhanced version transforms your Home Assistant into a powerful smart assistant like Alexa, featuring native LLM integration, voice controls, custom sounds, and a specialized Lovelace UI.

## ✨ Key "Pro" Features

- 🗣️ **Native Voice/LLM Intents**: Support for "Set", "Stop", and "Snooze" via Home Assistant Assist (Ollama, OpenAI, Gemini).
- 🔁 **Advanced Repetitions**: Set alarms for "Daily", "Weekdays", "Weekends", or specific days.
- 🔊 **Custom Alarm Sounds**: Specify a unique `.mp3` for each alarm.
- 🎨 **Lovelace "Alexa-Style" Card**: A dedicated UI card that auto-appears when an alarm is active and pulses red when ringing.
- 🇪🇸 **Native Spanish Support**: Full natural language processing for Spanish ("mañana a las 8", "entre semana", etc.).
- 🔄 **Smart Rescheduling**: Repeating alarms automatically schedule their next occurrence after being stopped.

## 🚀 Installation

### HACS (Recommended)

1. Open HACS.
2. Click on **Integrations**.
3. Click the three dots (top right) and select **Custom repositories**.
4. Add `https://github.com/rhythmcreative/hass-alarmclock` as a custom repository (Category: Integration).
5. Click **Install**.
6. Restart Home Assistant.

### Manual Installation

1. Copy the `custom_components/alarm_clock` directory to your Home Assistant's `custom_components` directory.
2. Restart Home Assistant.

## 🗣️ Voice & LLM Integration (Alexa Commands)

You can use voice or text via Assist. The integration exposes native intents:

- **Set Alarm**: *"Pon la alarma del dormitorio a las 7 de la mañana todos los días"* or *"Set kitchen alarm for 8pm with sound birds.mp3"*.
- **Stop Alarm**: *"Okay Nabu, para"* or *"Detén la alarma"*. (No name needed if it's ringing!)
- **Snooze**: *"Posponer la alarma"*.

## 🎨 Lovelace UI Card

We include a custom card that mirrors the Echo Show experience.

### Registration
Add the resource in **Settings > Dashboards > Resources**:
- **URL**: `/alarm-clock-ui/alarm-clock-card.js`
- **Type**: JavaScript Module

### Usage
```yaml
type: custom:alarm-clock-card
entity: switch.bedroom_alarm
status_entity: sensor.bedroom_status
time_entity: datetime.bedroom_time
repeat_entity: select.bedroom_repeat_pattern
auto_hide: true # Card only appears when an alarm is set
```

## 🛠️ Service Calls

```yaml
# Set alarm with pro features
service: alarm_clock.set_alarm
target:
  entity_id: switch.bedroom_alarm
data:
  time: "07:00"
  sound: "birds.mp3" # Optional
  repeat: "weekdays" # Optional (daily, weekdays, weekends)
```

## 📊 State Attributes & Sensors

- **Status Sensor**: Shows `set`, `unset`, `triggered`, or `snoozed`. Includes `alarm_sound` and `repeat` as attributes.
- **Select Entity**: Allows visual selection of repetition patterns.
- **Text Entity**: Change the default alarm sound easily.

## 📝 Example Automation (Triggering Sound)

```yaml
automation:
  - alias: "Play Custom Alarm Sound"
    trigger:
      platform: state
      entity_id: sensor.bedroom_status
      to: "triggered"
    action:
      - service: media_player.play_media
        target:
          entity_id: media_player.bedroom_speaker
        data:
          media_content_id: "media-source://media_source/local/{{ state_attr('sensor.bedroom_status', 'alarm_sound') }}"
          media_content_type: audio/mpeg
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Based on the original `hass-alarmclock` by [DGTLMagician](https://github.com/DGTLMagician/hass-alarmclock).
- Enhanced for the AI era by Gemini CLI.
