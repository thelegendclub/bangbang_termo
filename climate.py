import logging
import voluptuous as vol
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import TEMP_CELSIUS
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema(
    {
        vol.Required("name"): cv.string,
        vol.Required("temp_sensor"): cv.entity_id,
        vol.Required("switch"): cv.entity_id,
        vol.Optional("min_temp", default=40): vol.Coerce(float),
        vol.Optional("max_temp", default=50): vol.Coerce(float),
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([BangBangTermo(hass, config)])

class BangBangTermo(ClimateEntity):
    def __init__(self, hass, config):
        self._hass = hass
        self._name = config["name"]
        self._temp_sensor = config["temp_sensor"]
        self._switch = config["switch"]
        self._min_temp = config["min_temp"]
        self._max_temp = config["max_temp"]
        self._current_temp = None
        self._hvac_mode = HVAC_MODE_OFF

    @property
    def name(self):
        return self._name

    @property
    def hvac_mode(self):
        return self._hvac_mode

    @property
    def hvac_modes(self):
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        return self._current_temp

    @property
    def target_temperature(self):
        return self._max_temp

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE

    def update(self):
        state = self._hass.states.get(self._temp_sensor)
        if state:
            self._current_temp = float(state.state)

        if self._current_temp is not None:
            if self._current_temp < self._min_temp:
                self._hass.services.call("switch", "turn_on", {"entity_id": self._switch})
                self._hvac_mode = HVAC_MODE_HEAT
            elif self._current_temp >= self._max_temp:
                self._hass.services.call("switch", "turn_off", {"entity_id": self._switch})
                self._hvac_mode = HVAC_MODE_OFF
