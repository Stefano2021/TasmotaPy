from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import requests
from flask import Flask, jsonify, render_template, request

from config import (
    COMMAND_ENDPOINTS,
    DEVICE_ENDPOINTS,
    EZSP_COMMANDS,
    GATEWAY_PASSWORD,
    GATEWAY_URL,
    GATEWAY_USER,
    MOCK_DEVICES,
    USE_MOCK_DATA,
)

app = Flask(__name__, template_folder="templates", static_folder="static")


def gateway_request(method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
    """Generic HTTP helper for the Zigbee gateway."""
    if not GATEWAY_URL:
        return {"error": "GATEWAY_URL is not configured"}

    url = f"{GATEWAY_URL.rstrip('/')}{path}"
    auth = (GATEWAY_USER, GATEWAY_PASSWORD) if GATEWAY_USER and GATEWAY_PASSWORD else None
    headers = {"Content-Type": "application/json"}

    try:
        if method.upper() == "GET":
            response = requests.get(url, auth=auth, timeout=8, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=payload, auth=auth, timeout=8, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=payload, auth=auth, timeout=8, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, auth=auth, timeout=8, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()

        if not response.content:
            return {}

        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}
    except Exception as exc:
        return {"error": str(exc)}


def _coalesce(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", []):
            return value
    return None


def normalize_device(raw: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        return {}

    if "device" in raw and isinstance(raw["device"], dict):
        raw = raw["device"]

    ieee = _coalesce(raw.get("ieee"), raw.get("device_ieee"), raw.get("id"), raw.get("address"))
    name = _coalesce(raw.get("friendly_name"), raw.get("name"), raw.get("label"), ieee, "unknown")
    model = _coalesce(raw.get("model"), raw.get("type"), raw.get("manufacturer"), "unknown")
    endpoint = _coalesce(raw.get("endpoint"), raw.get("ep"), 1)
    state = _coalesce(raw.get("state"), raw.get("value"), raw.get("status"), "unknown")

    return {
        "device_id": str(ieee or name),
        "ieee": str(ieee or name),
        "friendly_name": str(name),
        "model": str(model),
        "endpoint": endpoint,
        "state": str(state),
        "raw": raw,
    }


def _extract_device_list(result: Any) -> List[Dict[str, Any]]:
    if isinstance(result, list):
        return [normalize_device(device) for device in result if isinstance(device, dict)]

    if isinstance(result, dict):
        for key in ("devices", "result", "items", "zigbee_devices", "data"):
            value = result.get(key)
            if isinstance(value, list):
                return [normalize_device(device) for device in value if isinstance(device, dict)]

        if isinstance(result.get("device"), dict):
            return [normalize_device(result["device"])]

    return []


def fetch_devices() -> List[Dict[str, Any]]:
    if USE_MOCK_DATA:
        return [normalize_device(entry) for entry in MOCK_DEVICES]

    for path in DEVICE_ENDPOINTS:
        payload = gateway_request("GET", path)
        if isinstance(payload, dict) and "error" in payload:
            continue
        devices = _extract_device_list(payload)
        if devices:
            return devices

    return []


def post_command(command: str, payload: Dict[str, Any], device_id: str, endpoint: int) -> Dict[str, Any]:
    if USE_MOCK_DATA:
        return {
            "ok": True,
            "device_id": device_id,
            "endpoint": endpoint,
            "command": command,
            "payload": payload,
            "status": "simulated",
        }

    request_body = {
        "device_id": device_id,
        "endpoint": endpoint,
        "command": command,
        "payload": payload or {},
    }

    for path in COMMAND_ENDPOINTS:
        result = gateway_request("POST", path, payload=request_body)
        if isinstance(result, dict) and "error" in result:
            continue
        if result:
            return {"ok": True, "result": result}

    return {"ok": False, "error": "Unable to send command to the gateway"}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/devices")
def api_devices():
    return jsonify(fetch_devices())


@app.get("/api/ezsp-commands")
def api_ezsp_commands():
    return jsonify(EZSP_COMMANDS)


@app.get("/api/status")
def api_status():
    return jsonify({
        "gateway_url": GATEWAY_URL,
        "mock_mode": USE_MOCK_DATA,
        "commands": EZSP_COMMANDS,
    })


@app.post("/api/command")
def api_command():
    data = request.get_json(silent=True) or {}
    device_id = data.get("device_id")
    command = data.get("command")
    payload = data.get("payload") or {}
    endpoint = int(data.get("endpoint") or 1)

    if not device_id or not command:
        return jsonify({"error": "device_id and command are required"}), 400

    if not isinstance(payload, dict):
        return jsonify({"error": "payload must be a JSON object"}), 400

    result = post_command(command, payload, device_id, endpoint)
    if result.get("ok"):
        return jsonify(result)
    return jsonify(result), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
