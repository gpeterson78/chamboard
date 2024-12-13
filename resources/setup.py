#!/bin/bash

# Chamboard Setup Script
# Automates the installation of prerequisites for the Chamboard project

echo "Starting Chamboard setup..."

# Update and upgrade system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "Installing Python and pip..."
sudo apt install -y python3 python3-pip

# Install required Python libraries
echo "Installing required Python libraries..."
pip3 install pillow spidev RPi.GPIO

# Install dependencies for Waveshare e-paper display
echo "Installing Waveshare e-paper display dependencies..."
sudo apt install -y python3-pil python3-numpy

# Install Firefox and Geckodriver
echo "Installing Firefox and Geckodriver..."
sudo apt install -y firefox-esr
GECKODRIVER_VERSION=$(curl -s https://github.com/mozilla/geckodriver/releases/latest | grep -oP 'v\K[0-9.]+')
wget "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux-arm7.tar.gz"
tar -xzf geckodriver-v${GECKODRIVER_VERSION}-linux-arm7.tar.gz
sudo mv geckodriver /usr/local/bin/
rm geckodriver-v${GECKODRIVER_VERSION}-linux-arm7.tar.gz

# Enable SPI interface
echo "Enabling SPI interface..."
sudo raspi-config nonint do_spi 0

# Cleanup
echo "Cleaning up unnecessary packages..."
sudo apt autoremove -y

echo "Chamboard setup completed! Please reboot your Raspberry Pi to apply all changes."