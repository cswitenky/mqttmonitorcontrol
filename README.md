This script allows you to control your monitor's brightness, input, and power state via [Home Assistant](https://www.home-assistant.io/) using [MQTT](https://en.wikipedia.org/wiki/MQTT) and [the DDC/CI protocol](https://en.wikipedia.org/wiki/Display_Data_Channel).

![image](screenshot.png)

Only supports Linux and single monitor setups.

## Pre-requisites
- Install the `paho-mqtt` library: `pip3 install paho-mqtt`
- Make sure `ddcutil` is installed and your user has permission to execute it without `sudo`.

## Installation
Copy the `mqttmonitorcontrol` directory to `/opt/`. The `main.py` file is your entry point. You can edit the configuration file to set your MQTT broker address, port, username, password, and topic.

Install this script as a systemd service to run on boot:
```ini
[Unit]
Description=MQTT Monitor Control
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/mqttmonitorcontrol/main.py
WorkingDirectory=/opt/mqttmonitorcontrol
User=cswitenky
Group=cswitenky
Restart=always
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
- Make sure `ddcutil` is installed and your user has permission to execute without `sudo`.

Copy `mqttmonitorcontrol` to `/opt/` and the `main.py` is your point of entry. You can edit the configuration file to set your MQTT broker address, port, username, password, and topic.

Install this script as a systemd service to run on boot.
```ini
[Unit]
Description=MQTT Monitor Control
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/mqttmonitorcontrol/main.py
WorkingDirectory=/opt/mqttmonitorcontrol
User=cswitenky
Group=cswitenky
Restart=always
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Future Improvements
- Add support for multiple monitors.
- Add support for volume control