class AlarmClockCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      this.innerHTML = `<ha-card style='box-shadow: none; background: none; border: none;'><div id='container'></div></ha-card>`;
      this.content = this.querySelector('#container');
    }

    const config = this.config;
    const entityId = config.entity;
    const baseId = entityId.split('.')[1].replace('_status', '');
    const timeEntity = config.time_entity || `datetime.${baseId}_time`;
    const repeatEntity = config.repeat_entity || `text.${baseId}_repeat_pattern`;
    
    const stateObj = hass.states[entityId];
    const timeObj = hass.states[timeEntity];
    const repeatObj = hass.states[repeatEntity];

    let timeDisplay = '--:--';
    if (timeObj && timeObj.state && !['unknown', 'unavailable'].includes(timeObj.state)) {
        const val = timeObj.state;
        timeDisplay = val.includes('T') ? val.split('T')[1].substring(0, 5) : val;
    }
    
    const repeatDisplay = repeatObj ? repeatObj.state : '';
    const isOn = stateObj && stateObj.state === 'on';

    this.content.innerHTML = `
      <style>
        #container {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 2px;
          padding: 8px;
          cursor: pointer;
        }
        ha-icon {
          --mdc-icon-size: 22px;
          color: ${isOn ? 'var(--primary-color)' : 'var(--disabled-text-color)'};
        }
        .time {
          font-size: 20px;
          font-weight: 500;
          color: var(--primary-text-color);
          line-height: 1.2;
        }
        .repeat {
          font-size: 11px;
          color: var(--secondary-text-color);
          line-height: 1;
        }
      </style>
      <ha-icon icon='mdi:alarm'></ha-icon>
      <div class='time'>${timeDisplay}</div>
      <div class='repeat'>${repeatDisplay}</div>
    `;

    this.content.onclick = () => {
        const event = new CustomEvent('hass-more-info', {
            detail: { entityId: timeEntity },
            bubbles: true, composed: true,
        });
        this.dispatchEvent(event);
    };
  }

  setConfig(config) {
    if (!config.entity) throw new Error('Define una entidad');
    this.config = config;
  }

  getCardSize() { return 1; }
}
customElements.define('alarm-clock-card', AlarmClockCard);