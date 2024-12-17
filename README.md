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

| **Item**                              | **Description**                                      | **Link**                               |
|---------------------------------------|----------------------------------------------------|---------------------------------------|
| Raspberry Pi Zero 2 W                 | Compact single-board computer                      | [Buy on PiShop](https://www.microcenter.com/product/643085/raspberry-pi-zero-2-w)  |
| Waveshare 7.5" E-Paper Display (V2)   | 7.5-inch e-ink display for low-power visuals       | [Buy on Waveshare](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm) |
| Optional: Case / 3D Printed Frame     | Custom 3D printed frame to house the display       | See [3D Printed Frame](#3d-printed-frame) |

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

This is a future feature and currently serves no purpose.  On the todo list is to update the setup script to point the screenshot at the internal website, and an input for a wordpress thread or custom URL to use.  This will also eventually have a web based configuration, a groin-grabbingly simple one, but functional enough so that it can be configured from a phone.


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

## 3D Printed Frame
To make Chamboard look great in your home, you can use a custom 3D-printed frame. You can find the STL file here:

[3D Printed Frame on Thingiverse](https://example.com)

---

## Future Plans
- Add a web-based configuration tool for easier setup.
- Allow message input directly from the local web server.
- Instructions/setup options for tailscale or other remote access.
---

### Contributions
Feel free to contribute to the project by submitting issues, pull requests, or feature suggestions.

---

### License
This project is licensed under the MIT License.

---

Thank you for using Chamboard! 😊
