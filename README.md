# TasmotaPy

Python web dashboard for a Tasmota2Zigbee / ZB-GW03 gateway.

This project provides a small Flask app that lists Zigbee devices and lets you send EZSP-style commands from a browser.

## Features

- Device list from a Tasmota2Zigbee gateway
- Browser-based dashboard
- Generic EZSP command dispatcher
- Ready for REST/MQTT gateway integrations
- Mock mode for local demo/testing

## Requirements

- Python 3.10+
- Flask
- requests

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://localhost:5000
```

## Configuration

Edit `config.py` and set your gateway URL and credentials:

```python
GATEWAY_URL = "http://192.168.1.50"
GATEWAY_USER = "admin"
GATEWAY_PASSWORD = "password"
USE_MOCK_DATA = False
```

If `USE_MOCK_DATA` is `True`, the app shows sample devices even if the gateway is unavailable. This is useful for testing the UI.

## API

Available endpoints:

- `GET /api/devices` -> device list
- `GET /api/ezsp-commands` -> supported command names
- `POST /api/command` -> send a command to the gateway
- `GET /api/status` -> gateway status

Example request:

```bash
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "00:12:4b:00:01:02:03:04",
    "command": "on",
    "payload": {"state": true},
    "endpoint": 1
  }'
```

## Notes

The exact Tasmota2Zigbee API depends on your gateway firmware and how it exposes Zigbee commands. This project is intentionally generic: it tries common REST paths first and lets you configure command names and payloads in one place.

If your gateway exposes a different endpoint, edit `DEVICE_ENDPOINTS` and `COMMAND_ENDPOINTS` in `config.py`.
