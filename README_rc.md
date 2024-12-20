# Chamboard - E-Paper Reminder Board

![Chamboard Logo](./docs/chamboard.jpeg)

**Version:** 0.7

Chamboard is an e-paper display designed to act as a reminder board for an aging parent. This project allows you to display messages, reminders, or notes pulled dynamically from a WordPress site, an arbitrary URL, or a built-in local web server.

Initially inspired by Jan Miksovsky's [momboard](https://github.com/JanMiksovsky/momboard), this project has evolved with custom hardware and software to better suit its purpose.

---

## Table of Contents
- [Chamboard - E-Paper Reminder Board](#chamboard---e-paper-reminder-board)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Parts List](#parts-list)
  - [Setup Instructions](#setup-instructions)
    - [1. Prepare the Raspberry Pi](#1-prepare-the-raspberry-pi)
    - [2. Download and Run Chamboard](#2-download-and-run-chamboard)
    - [3. Enable the Web Server (Optional)](#3-enable-the-web-server-optional)
    - [4. Reboot the Device](#4-reboot-the-device)
  - [How It Works](#how-it-works)
  - [Usage](#usage)
    - [Settings Overview](#settings-overview)
    - [Logs and Debugging](#logs-and-debugging)
  - [New Features](#new-features)
  - [Future Plans](#future-plans)
  - [3D Printed Frame](#3d-printed-frame)
  - [License](#license)

---

## Overview
Chamboard is designed to:
- Display messages on a 7.5" Waveshare e-paper display.
- Dynamically pull reminders from a WordPress site, arbitrary URLs, or a local web server.
- Be lightweight, power-efficient, and easy to set up.

The project is built with Python and tested on a **Raspberry Pi Zero 2 W**.

---

## Parts List
| **Item**                                                                                  | **Description**                                                |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [Raspberry Pi Zero 2 W](https://www.microcenter.com/product/643085/raspberry-pi-zero-2-w) | Compact single-board computer                                  |
| [Waveshare 7.5" E-Paper Display (V2)](https://www.waveshare.com/7.5inch-e-Paper-HAT.htm)  | 7.5-inch e-ink display for low-power visuals                   |
| [3D Printed Frame](https://makerworld.com/en/models/787533)                               | 3D printed frame to house the display                         |

---

## Setup Instructions

### 1. Prepare the Raspberry Pi
- Flash **Raspberry Pi OS Lite (64-bit)** onto your SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
- Enable SSH and Wi-Fi during setup (recommended for headless configuration).

### 2. Download and Run Chamboard
```bash
wget -O chamboard.zip https://github.com/gpeterson78/chamboard/archive/refs/heads/main.zip
unzip chamboard.zip
mv chamboard-main chamboard  # Rename for consistency
```

Run the setup script:
```bash
sudo chmod +x chamboard/setup.sh
./chamboard/setup.sh
```

### 3. Enable the Web Server (Optional)
During setup, you will be asked if you'd like to enable the local web server. This serves:
- **Static Content**: Located in `/docs`.
- **Dynamic Content**: Provides API endpoints for configuration and message management.

Access it via:
```
http://<raspberry-pi-ip>:8080
```

### 4. Reboot the Device
Once setup is complete, the device will reboot, and the Chamboard script will begin capturing content and displaying it on the e-paper screen.

---

## How It Works
1. **Dynamic Configuration**: The settings page allows switching between:
   - Pulling messages from a WordPress REST API.
   - Capturing screenshots of any arbitrary URL.
   - Using the built-in local web server for fallback messages.
2. **Screenshot Capture**: Uses Playwright (WebKit) to capture screenshots and display them on the e-paper display.
3. **Local Message Handling**: Supports:
   - Adding messages via `/add_comment`.
   - Deleting the last message via `/delete_last_comment`.
   - Fetching messages via `/comments`.
   - Configuring settings via `/config`.
4. **Automatic Refresh**: Cron jobs refresh the display at configurable intervals.

---

## Usage
### Settings Overview
Chamboard provides a user-friendly settings page to:
1. **Input URL to Scrape**:
   - Enter a WordPress REST API URL (e.g., `https://example.com/wp-json/wp/v2/comments?post=1234`).
   - Enter an arbitrary URL for screenshot display.
2. **Use Internal Webserver**:
   - Enables the local server for message input and fallback.
   - Dynamically greys out and links with "Use Internal Message Server."
3. **Use Internal Message Server**:
   - Fetches and displays messages stored locally.
   - Messages can be added or deleted via the web interface or APIs.

### Logs and Debugging
1. **Message Log**: Displays fetched messages in a scrollable section.
2. **Screenshot Display**: Shows the latest captured screenshot when not fetching WordPress messages.
3. **Troubleshooting Logs**: Check the `logs/` directory for runtime errors or connectivity issues.

---

## New Features
- **Dynamic URL Handling**: Automatically switches between WordPress API and arbitrary URLs for content display.
- **Local Webserver**: Acts as a fallback for messages and allows remote management.
- **Interactive API**:
  - Add messages: `/add_comment`
  - Delete last message: `/delete_last_comment`
  - Fetch messages: `/comments`
  - Configure settings: `/config`
- **Enhanced UI**:
  - Greyed-out checkboxes dynamically enforce valid settings.
  - Clear distinction between message log and screenshot modes.

---

## Future Plans
- Add direct message input via the local web server.
- Implement a mobile-friendly web-based configuration interface.
- Provide setup options for Tailscale or other remote access tools.
- Optimize performance and extend support to additional e-paper displays.

---

## 3D Printed Frame
Chamboard is designed to fit into a 3D-printed frame for clean presentation. See the [3D Printed Frame](https://makerworld.com/en/models/787533) section for more details.

---

## License
This project is licensed under the MIT License.

Thank you for using Chamboard! 😊
