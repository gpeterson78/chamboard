# Chamboard - E-Paper Reminder Board

![Chamboard Logo](./docs/chamboard.jpeg)

Chamboard is an e-paper display designed to act as a reminder board for an aging parent. It dynamically pulls messages, reminders, or notes from a WordPress site or a built-in local web server.  Chamboard is named for my mom, lovingly nickamed Chambray.  When you build such a project, is there any other name I could have used?

This whole thing started when I stumbled across Jan Miksovsky's [Momboard](https://github.com/JanMiksovsky/momboard). His project is great—polished, professional, and way more thought-out than my little hack. But I’m a nerd who likes to DIY, and I’ve got Raspberry Pis and Linux servers strewn all over my house. So instead of dropping money on an expensive e-reader, I decided to cobble together my own e-paper display.

---

## The Story Behind Chamboard

At first, I thought I’d just modify Momboard for my setup. That plan fell apart pretty quickly when I realized I’d have to use expensive hardware. I’m cheap and stubborn, so I figured I could make something work with what I had on hand or what I could hack together cheaply. I've got all these pi's laying around so I picked up a Waveshare e-paper display and assumed it would work like a regular (albeit slow) display.

Spoiler: it doesn’t. Turns out, you need to push images to the display via SPI. This was new territory for me, but I’ve been meaning to learn Python anyway, and the Waveshare display has all kinds of Python support. Challenge accepted. Before I knew it, I had the thing displaying images and I was pretty impressed with myself.

Then came the question of where to get the content. While Momboard has a JSON host, I wanted something simpler (and let’s be honest—lazier). I already host my own WordPress blog, figured there had to be a way to use it as the backend. So I figured I'd find a way to just point the script at the WordPress API and scrape comments from a page. It wound up working like a charm.

At this point, I had a fully operational display board. It was fun, functional, and, well, completely useless unless you happen to run a WordPress blog hacked together like mine. Clearly, it needed a backend of its own.

I figured Python was already in the picture, so why not see where else I could take it.  First up, I wanted to have an internal web host so that I didn't have to rely on gitlab.  That was easy, so should the rest be, right?  I mean, in truth it was, but man, it took a while.  Backend wasn't too difficult but getting everything all tied together was a chore that took the majority of the time building this little thing.  But, in the end, it pretty much works as I intended.  Read on for the details in case you want to put together one of your own.

None of this would’ve been possible without AI—because let’s face it, we live in the future, and I’ll take all the help I can get.

---

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
To build Chamboard, you’ll need:

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
During setup, you’ll be asked if you want to enable the local web server. If enabled, it’ll serve static content from `/docs` on port **8080**.  There's really no reason not to.

Access it at:
```
http://<raspberry-pi-ip>:8080
or
http://<rasberry-pi-ip>:8080/settings
```

### 4. Reboot the Device
Once setup is complete, the device will reboot, and Chamboard will start displaying content.

---

## How It Works
1. **Screenshot Capture**: A Python script uses Playwright (WebKit) to capture screenshots of a specified URL.
2. **Display on E-Paper**: The screenshot is resized and displayed on the Waveshare 7.5" e-paper display.
3. **Fallback Server**: If no URL is available, Chamboard serves fallback content via its built-in static web server.
4. **Automatic Refresh**: Cron jobs are set up to refresh the display every 30 minutes.

---

## Usage
1. Power on the Raspberry Pi and connect it to the internet.
2. By default, Chamboard will:
   - Pull content from the configured WordPress site.
   - Refresh the display every 30 minutes.
3. Access the internal web server at:
   ```
   http://<raspberry-pi-ip>:8080
   ```
4. Settings are available at http://<raspberry-pi-ip>:8080/settings.html or just click on the Chamboard logo.
5. Logs are stored in the `logs/` directory for troubleshooting.
6. Chamboard is designed for local administration and should not be exposed to the internet because  it is hilariously insecure (although it needs an internet connection for remote wordpress scraping).  For remote management, it's suggestted to setup Tailscale or a similar secure service.  this is at your own risk.

---

## 3D Printed Frame
To house your Chamboard, you can use a 3D-printed frame. The one I used is available on [Makerworld](https://makerworld.com/en/models/787533).

---

### Contributions
Chamboard is meant to be hacked, shared, and enjoyed. Got suggestions? Feedback? Bring it on—just don’t tell me how insecure it is. I know, it’s a [snand](https://www.snand.org) project, after all.

---

### License
This project is licensed under the MIT License.

---

Thanks for checking out Chamboard! 😊

