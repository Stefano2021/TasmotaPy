GATEWAY_URL = "http://192.168.1.50"
GATEWAY_USER = "admin"
GATEWAY_PASSWORD = "password"
USE_MOCK_DATA = True

DEVICE_ENDPOINTS = [
    "/api/devices",
    "/api/zigbee/devices",
    "/api/devices/all",
    "/api/zigbee/network/devices",
]

COMMAND_ENDPOINTS = [
    "/api/zigbee/command",
    "/api/devices/command",
    "/api/command",
]

EZSP_COMMANDS = [
    "permit_join",
    "network_status",
    "read_attribute",
    "write_attribute",
    "bind",
    "unbind",
    "identify",
    "on",
    "off",
    "toggle",
    "set_level",
    "leave_network",
    "reset",
    "ping",
]

MOCK_DEVICES = [
    {
        "friendly_name": "Lampada cucina",
        "ieee": "00:12:4B:00:01:02:03:04",
        "model": "OnOffLight",
        "endpoint": 1,
        "state": "on",
        "type": "light",
    },
    {
        "friendly_name": "Sensore temperatura",
        "ieee": "00:12:4B:00:01:02:03:05",
        "model": "TemperatureSensor",
        "endpoint": 1,
        "state": "ok",
        "type": "sensor",
    },
    {
        "friendly_name": "Pulsante ingresso",
        "ieee": "00:12:4B:00:01:02:03:06",
        "model": "OnOffSwitch",
        "endpoint": 1,
        "state": "idle",
        "type": "switch",
    },
]
