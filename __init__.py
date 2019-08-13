"""
Component for interacting with a SnapAV Binary-Brand Media Over IP
(MoIP) system for video distribution.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/binarymoip/
"""
# import asyncio
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers import discovery
# from homeassistant.helpers.entity import Entity

DOMAIN = 'binarymoip'
DEVICES = 'binarymoip_devices'

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the Binary MoIP component."""
    from pybinarymoip import MoIP

    hass.data[DEVICES] = {'media_player': [],
                          'sensor': []}

    moip_config = config[DOMAIN]
    host = moip_config[CONF_HOST]
    username = moip_config.get(CONF_USERNAME)
    password = moip_config.get(CONF_PASSWORD)

    try:
        m = MoIP(host, username, password)
        m.connect()
        for mp in m.receivers:
            _LOGGER.info("adding MoIP Rx %s", mp)
            hass.data[DEVICES]['media_player'].append(mp)
        for s in m.transmitters:
            _LOGGER.info("adding MoIP Tx %s", s)
            hass.data[DEVICES]['sensor'].append(s)
    except Exception as e:
        _LOGGER.error("Could not setup MoIP at %s - %s", host, e)

    hass.data[DOMAIN] = m

    discovery.load_platform(hass, 'media_player', DOMAIN, None, config)
    discovery.load_platform(hass, 'sensor', DOMAIN, None, config)

    return True
