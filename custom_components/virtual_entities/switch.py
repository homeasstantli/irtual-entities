from homeassistant.components.switch import SwitchEntity

SWITCHES = [
    ("My Switch One", "my_switch_one"),
    ("My Switch Two", "my_switch_two"),
]

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([
        VirtualSwitch(hass, name, uid) for name, uid in SWITCHES
    ])

class VirtualSwitch(SwitchEntity):
    def __init__(self, hass, name, unique_id):
        self._hass = hass
        self._name = name
        self._unique_id = unique_id
        self._state = False

    @property
    def name(self): return self._name
    @property
    def unique_id(self): return self._unique_id
    @property
    def is_on(self): return self._state
    @property
    def should_poll(self): return False

    async def async_turn_on(self, **kwargs):
        self._state = True
        self._hass.bus.async_fire(f"virtual_switch_{self._unique_id}_on")
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._state = False
        self._hass.bus.async_fire(f"virtual_switch_{self._unique_id}_off")
        self.async_write_ha_state()
