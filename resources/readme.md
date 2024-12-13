# Chamboard Resources

## everything in this directory is currently in progress and should be considered completely broken.

This folder contains the scripts and resources required to set up and operate the Chamboard project on a Raspberry Pi Zero 2 W.

## Overview

The Chamboard project is designed to display family messages on a Waveshare 7.5" e-paper display. This folder includes all necessary files to streamline setup and ensure the system functions as intended.

## Files

- **chamboard.py**  
  The main Python script that captures an image (e.g., a screenshot of a target webpage) and sends it to the e-paper display.

- **setup.sh** *(in development)*  
  A shell script to automate the installation and configuration of the Chamboard environment. This script will handle:
  - Installing required dependencies
  - Configuring Raspberry Pi settings for the e-paper display
  - Setting up system services or cron jobs to run `chalkboard.py` automatically

- **README.md**  
  The file you're reading now, providing an overview of the resources and their usage.

## Usage

1. Clone the Chamboard repository to your Raspberry Pi.
2. Navigate to this `resources` folder.
3. Once `setup.sh` is available, run it to configure your Raspberry Pi:
   ```bash
   ./setup.sh