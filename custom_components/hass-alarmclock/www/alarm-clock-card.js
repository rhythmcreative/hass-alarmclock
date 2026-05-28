class AlarmClockCard extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (!this.content) {
      this.innerHTML = `
        <ha-card>
          <div id="container"></div>
        </ha-card>
      `;
      this.content = this.querySelector('#container');
    }

    const config = this.config;
    const entityId = config.entity;
    const statusEntity = config.status_entity;
    const timeEntity = config.time_entity;
    const repeatEntity = config.repeat_entity;
    
    const stateObj = hass.states[entityId];
    const statusObj = hass.states[statusEntity];
    const timeObj = hass.states[timeEntity];
    const repeatObj = hass.states[repeatEntity];

    if (!stateObj || !statusObj) {
      this.content.innerHTML = "Entity not found";
      return;
    }

    const status = statusObj.state;
    const isUnset = status === 'unset';
    const isTriggered = status === 'triggered';
    
    if (config.auto_hide && isUnset) {
      this.style.display = 'none';
      return;
    } else {
      this.style.display = 'block';
    }

    const alarmTime = timeObj ? timeObj.state : '--:--';
    const timeDisplay = alarmTime.includes('T') ? alarmTime.split('T')[1].substring(0, 5) : alarmTime;
    const repeatDisplay = repeatObj ? repeatObj.state : 'No repetir';

    this.content.innerHTML = `
      <style>
        #container {
          padding: 12px 16px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          background: ${isTriggered ? 'rgba(255, 0, 0, 0.2)' : 'var(--ha-card-background, var(--card-background-color, white))'};
          border-radius: var(--ha-card-border-radius, 12px);
          transition: all 0.5s ease;
          border: 1px solid rgba(255,255,255,0.1);
        }
        .info { flex: 1; cursor: pointer; }
        .time { font-size: 32px; font-weight: 600; line-height: 1; color: var(--primary-text-color); }
        .repeat { font-size: 13px; color: var(--secondary-text-color); margin-top: 4px; display: flex; align-items: center; gap: 4px; }
        .status { font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--primary-color); font-weight: 800; margin-bottom: 4px; }
        .controls { display: flex; gap: 10px; }
        .btn {
          border: none;
          padding: 12px 24px;
          border-radius: 24px;
          font-weight: bold;
          cursor: pointer;
          font-size: 14px;
          text-transform: uppercase;
          background: var(--primary-color);
          color: white;
          box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .btn-stop { background: #f44336; }
        .btn-snooze { background: #ff9800; color: black; }
        .pulse { animation: pulse-red 1.5s infinite; }
        @keyframes pulse-red {
          0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.7); }
          70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(244, 67, 54, 0); }
          100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }
        }
      </style>
      <div class="info" id="info-area">
        <div class="status">${status}</div>
        <div class="time">${timeDisplay}</div>
        <div class="repeat">
            <ha-icon icon="mdi:repeat" style="--mdc-icon-size: 14px;"></ha-icon>
            ${repeatDisplay}
        </div>
      </div>
      <div class="controls">
        ${isTriggered ? `
          <button class="btn btn-snooze" id="snooze-btn">SNOOZE</button>
          <button class="btn btn-stop pulse" id="stop-btn">STOP</button>
        ` : `
          <ha-switch id="toggle-sw" ${status === 'set' ? 'checked' : ''}></ha-switch>
        `}
      </div>
    `;

    const infoArea = this.content.querySelector('#info-area');
    if (infoArea) {
        infoArea.onclick = () => {
            const event = new CustomEvent("hass-more-info", {
                detail: { entityId: timeEntity },
                bubbles: true,
                composed: true,
            });
            this.dispatchEvent(event);
        };
    }

    const toggleSw = this.content.querySelector('#toggle-sw');
    if (toggleSw) {
        toggleSw.onclick = () => hass.callService('switch', 'toggle', { entity_id: entityId });
    }
    const stopBtn = this.content.querySelector('#stop-btn');
    if (stopBtn) {
        stopBtn.onclick = () => hass.callService('alarm_clock', 'stop', { entity_id: entityId });
    }
    const snoozeBtn = this.content.querySelector('#snooze-btn');
    if (snoozeBtn) {
        snoozeBtn.onclick = () => hass.callService('alarm_clock', 'snooze', { entity_id: entityId });
    }
  }

  setConfig(config) {
    this.config = config;
  }

  getCardSize() {
    return 1;
  }
}

customElements.define('alarm-clock-card', AlarmClockCard);
