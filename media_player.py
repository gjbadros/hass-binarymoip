"""Binary MoIP Receiver as a Media Player."""
import logging

from homeassistant.components.media_player import (
    MediaPlayerDevice,
)
from homeassistant.components.media_player.const import (
    SUPPORT_SELECT_SOURCE,
)
from ..binarymoip import DEVICES

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE_CLASS = 'moip'
DEVICE_ID = 'pybinarymoip'
DEVICE_NAME = 'Binary MoIP Rx'

ICON = 'mdi:television'

SUPPORTED_COMMANDS = SUPPORT_SELECT_SOURCE


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the MoIP receivers as media_player devices."""
    devs = []
    for mp in hass.data[DEVICES]['media_player']:
        hass_mp = MoIP_MediaPlayer_Rx(mp)
        devs.append(hass_mp)

    add_devices(devs, True)
    _LOGGER.debug("MoIP Added %s", devs)
    return True


class MoIP_MediaPlayer_Rx(MediaPlayerDevice):
    """Media Player implementation for MoIP Receiver."""

    def __init__(self, moip_rx):
        """Initialize MoIP Rx device."""
        self._rx = moip_rx

#    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update(self):
        """Retrieve latest state of the device."""
        self._rx._mc._update_inputs()

    @property
    def state(self):
        """Return the state of the device."""
        return self._rx._input and self._rx._input.num

    @property
    def name(self):
        """Return the name of the device."""
        return "moip_rx_" + self._rx.name

    @property
    def source(self):
        """Return current input of the device."""
        return self._rx._input and self._rx._input.name

    @property
    def source_list(self):
        """Return list of available inputs of the device."""
        ai = []
        for t in self._rx._mc.transmitters:
            ai.append(t.name)
        return ai

    @property
    def supported_features(self):
        """Flag device features that are supported."""
        return SUPPORTED_COMMANDS
