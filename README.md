# Chamboard - E-Paper Reminder Board

![Chamboard Logo](./docs/chamboard.jpeg)

Chamboard is an e-paper display designed to act as a reminder board for an aging parent. This project allows you to display messages, reminders, or notes pulled dynamically from a WordPress site or a built-in local web server.

Initially inspired by Jan Miksovsky's [momboard](https://github.com/JanMiksovsky/momboard), this project has taken a new direction with custom hardware and software to better suit its purpose.

## Table of Contents
1. [Overview](#overview)
2. [Parts List](#parts-list)
3. [Setup Instructions](#setup-instructions)
4. [How It Works](#how-it-works)
5. [Usage](#usage)
6. [3D Printed Frame](#3d-printed-frame)
7. [Future Plans](#future-plans)

---

## Overview
Chamboard is designed to:
- Display messages on a 7.5" Waveshare e-paper display.
- Pull reminders dynamically from a WordPress site (or other URL).
- Optionally run a built-in local web server for fallback content.
- Be lightweight, power-efficient, and easy to set up.

The project is built with Python and tested on a **Raspberry Pi Zero 2 W**.

---

## Parts List
To build Chamboard, you will need the following components (these are **NOT** affiliated links, just examples):

| **Item**                                                                                  | **Description**                                                |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [Raspberry Pi Zero 2 W](https://www.microcenter.com/product/643085/raspberry-pi-zero-2-w) | Compact single-board computer                                  |
| [Waveshare 7.5" E-Paper Display (V2)](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm)  | 7.5-inch e-ink display for low-power visuals                   |
| [3D Printed Frame](https://makerworld.com/en/models/787533)                               | 3D printed frame to house the display - the one I used anyway. |

---

## Setup Instructions

### 1. Prepare the Raspberry Pi
- Flash **Raspberry Pi OS Lite (64-bit)** onto your SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
- Enable SSH and Wi-Fi during setup (recommended for headless configuration).

### 2. Download and Run Chamboard
1. Download the Chamboard repository:
   ```bash
   wget -O chamboard.zip https://github.com/gpeterson78/chamboard/archive/refs/heads/main.zip
   unzip chamboard.zip
   mv chamboard-main chamboard  # Rename for consistency
   ```
2. Run the setup script:
   ```bash
   sudo chmod +x chamboard/setup.sh
   ./chamboard/setup.sh
   ```
3. Follow the prompts during the installation.

### 3. Enable the Web Server (Optional)
During setup, you will be asked if you'd like to enable the local web server. If enabled, this will serve the static content located in `/docs` on port **8080**.

Access it via:
```
http://<raspberry-pi-ip>:8080
```

This feature is planned for future functionality and currently serves as a placeholder.[^1]

### 4. Reboot the Device
Once setup is complete, the device will reboot and the Chamboard script will begin capturing content and displaying it on the e-paper screen.

---

## How It Works
1. **Screenshot Capture**: A Python script uses Playwright (WebKit) to capture screenshots of a specified URL.
2. **Display on E-Paper**: The screenshot is resized and displayed on the Waveshare 7.5" e-paper display.
3. **Fallback Server**: If no URL is available, Chamboard serves fallback content via its built-in static web server.
4. **Automatic Refresh**: Cron jobs are set up to refresh the display every 30 minutes.

---

## Usage
1. Ensure the Raspberry Pi is powered on and connected to the internet.
2. By default, Chamboard will:
   - Pull content from the configured WordPress site.
   - Refresh the display every 30 minutes.
3. Access the fallback web server at:
   ```
   http://<raspberry-pi-ip>:8080
   ```
4. Logs are stored in the `logs/` directory for troubleshooting.
5. Recommended: setup a remote access for management via something like tailscale.

---

### Contributions
Feel free to contribute to the project by submitting issues, pull requests, or feature suggestions.

---

### License
This project is licensed under the MIT License.

---

Thank you for using Chamboard! 😊

[^1]: future plans and additions:
  - Allow message input directly from the local web server.
  - Add input options for a WordPress thread/custom URL to pull content from.
  - Implement a web-based configuration interface that is simple, functional, and accessible via a phone.
  - Instructions/setup options for tailscale or other remote access.
