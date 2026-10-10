# TasmotaPy - Zigbee Web Controller

Uno script Python che genera una pagina web interattiva per controllare dispositivi Zigbee connessi a un dispositivo **ZB-GW03** con **Tasmota2Zigbee**.

## Funzionalità

- 📱 **Dashboard Web**: Visualizza tutti i dispositivi Zigbee connessi
- 🎮 **Controllo Dispositivi**: Esegui comandi supportati da EZSP
- 🔍 **Monitoraggio Real-time**: Stato dei dispositivi in tempo reale
- 🔌 **Integrazione Tasmota**: Comunica con il gateway via HTTP/MQTT

## Requisiti

- Python 3.8+
- Dispositivo ZB-GW03 con Tasmota2Zigbee
- Connessione di rete al gateway

## Installazione

```bash
git clone https://github.com/Stefano2021/TasmotaPy.git
cd TasmotaPy
pip install -r requirements.txt
```

## Utilizzo

```bash
python app.py
```

Accedi a: `http://localhost:5000`

## Configurazione

Modifica `config.py` con i dettagli del tuo gateway:

```python
GATEWAY_IP = "192.168.1.100"  # IP del tuo ZB-GW03
GATEWAY_PORT = 80
GATEWAY_USER = "admin"
GATEWAY_PASSWORD = "password"
```

## Struttura Progetto

```
TasmotaPy/
├── app.py                 # App Flask principale
├── config.py              # Configurazione
├── requirements.txt       # Dipendenze Python
├── tasmota_client.py      # Client per comunicare con Tasmota
├── zigbee_device.py       # Modello dispositivo Zigbee
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── index.html         # Dashboard
    └── device.html        # Dettagli dispositivo
```

## API REST

- `GET /api/devices` - Lista dispositivi
- `GET /api/devices/<address>` - Dettagli dispositivo
- `POST /api/devices/<address>/command` - Esegui comando
- `GET /api/status` - Status gateway

## License

MIT
