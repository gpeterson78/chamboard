#!/bin/bash

# Exit on any error
set -e

# Variables
PROJECT_DIR="$HOME/chamboard"
VENV_DIR="$PROJECT_DIR/venv"
DOCS_DIR="$PROJECT_DIR/docs"
LOG_DIR="$PROJECT_DIR/logs"
MOTD_INSTRUCTIONS="/etc/motd.d/setup-instructions"
WEB_SERVICE_FILE="/etc/systemd/system/chamboard_webserver.service"
PYTHON_PACKAGES="python3 python3-pip python3-full python3-venv python3-flask python3-flask-cors
CRON_INTERVAL="*/30 * * * *"  # Every 30 minutes
SCRIPT_PATH="$PROJECT_DIR/resources/chamboard.py"  # Full path to chamboard.py
CURRENT_LOG="$LOG_DIR/chamboard.log"  # Current log file
ARCHIVE_RETENTION=3  # Number of archived logs to retain

# Check if SPI is enabled
echo "Checking if SPI is enabled..."
if ! ls /dev/spidev0.* > /dev/null 2>&1; then
    echo "ERROR: SPI is not enabled."
    echo "Please enable SPI using the following steps:"
    echo "1. Run 'sudo raspi-config'."
    echo "2. Navigate to 'Interface Options'."
    echo "3. Select 'SPI' and enable it."
    echo "4. Reboot the Raspberry Pi (optional but recommended)."
    echo "Exiting setup."
    exit 1
else
    echo "SPI is enabled."
fi

# Ensure the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "ERROR: chamboard.py not found, please ensure you have downloaded or cloned the full repo: https://github.com/gpeterson78/chamboard."
    exit 1
fi

# Ensure the script is not run as root
if [ "$(id -u)" -eq 0 ]; then
    echo "ERROR: Do not run this script with sudo."
    echo "Please run as a regular user. The script will use sudo where necessary."
    exit 1
fi

# Update system and install missing packages
echo "Updating and upgrading the system..."
sudo apt update && sudo apt upgrade -y

echo "Ensuring required Python packages are installed..."
for package in $PYTHON_PACKAGES; do
    if ! dpkg -l | grep -qw "$package"; then
        echo "Installing $package..."
        sudo apt install -y "$package"
    else
        echo "$package is already installed."
    fi
done

# Install minimal system dependencies for WebKit
echo "Installing minimal system dependencies for WebKit..."
sudo apt install -y \
    libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav \
    libxslt1.1 libwoff1 libvpx7 libevent-2.1-7 libopus0 \
    libwebpdemux2 libharfbuzz-icu0 libwebpmux3 libenchant-2-2 \
    libsecret-1-0 libhyphen0 libwayland-server0 libgbm1 libgles2 \
    libx264-dev flite libmanette-0.2-0

# Verify Python and pip versions
echo "Verifying Python and pip versions..."
python3 --version

if ! command -v pip3 &>/dev/null; then
    echo "pip3 not found. Installing pip3..."
    sudo apt install -y python3-pip
else
    echo "pip3 version:"
    pip3 --version
fi

# Create project directory if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Creating project directory at $PROJECT_DIR..."
    mkdir -p "$PROJECT_DIR"
else
    echo "Project directory $PROJECT_DIR already exists."
fi
cd "$PROJECT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment $VENV_DIR already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install Playwright and WebKit
echo "Installing Playwright and WebKit..."
pip install --upgrade pip  # Upgrade pip to the latest version
pip install playwright
playwright install webkit  # Install only WebKit binary

# Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate

# Add the virtual environment's bin directory to PATH if not already present
if ! grep -q "$VENV_DIR/bin" ~/.bashrc; then
    echo "Adding virtual environment to PATH in .bashrc..."
    echo "export PATH=\$PATH:$VENV_DIR/bin" >> ~/.bashrc
else
    echo "Virtual environment bin directory already in PATH."
fi

# Enable SPI in /boot/config.txt
echo "Enabling SPI configuration..."
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "SPI is not enabled. Enabling it now..."
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt > /dev/null
else
    echo "SPI is already enabled in /boot/config.txt."
fi

# Load the SPI kernel module
if ! lsmod | grep -q spi_bcm2835; then
    echo "Loading SPI kernel module..."
    sudo modprobe spi_bcm2835
else
    echo "SPI kernel module is already loaded."
fi

# Add the SPI kernel module to load at boot
if ! grep -q "spi_bcm2835" /etc/modules; then
    echo "Adding SPI kernel module to /etc/modules..."
    echo "spi_bcm2835" | sudo tee -a /etc/modules > /dev/null
else
    echo "SPI kernel module is already configured to load at boot."
fi

# Verify SPI device files
echo "Checking for SPI device files..."
if ! ls /dev/spidev0.* > /dev/null 2>&1; then
    echo "ERROR: SPI device files are not available. SPI may not be properly enabled."
    echo "Ensure that SPI is enabled in /boot/config.txt and that the Raspberry Pi has been rebooted."
    exit 1
else
    echo "SPI device files are available: $(ls /dev/spidev0.*)"
fi

# Inform the user that a reboot is required
# echo "SPI has been enabled. A reboot is required to apply changes."

# Install Python libraries for e-paper display
echo "Installing Python libraries for the e-paper display..."
source "$VENV_DIR/bin/activate"
pip install Pillow spidev RPi.GPIO gpiozero lgpio

# Download and install Waveshare e-Paper library as a ZIP
echo "Downloading and installing Waveshare e-Paper library..."
wget -O /tmp/e-Paper.zip https://github.com/waveshare/e-Paper/archive/refs/heads/master.zip
unzip -o /tmp/e-Paper.zip -d /tmp/e-Paper
pip install /tmp/e-Paper/e-Paper-master/RaspberryPi_JetsonNano/python

# Clean up temporary files
rm -rf /tmp/e-Paper.zip /tmp/e-Paper

# Deactivate virtual environment
deactivate

# # Webserver Setup
# if systemctl is-active --quiet chamboard_webserver.service; then
#     echo "The Chamboard webserver is already running."
#     read -p "Do you want to keep it running? (y/n): " KEEP_WEBSERVER
#     if [[ "$KEEP_WEBSERVER" =~ ^[Nn]$ ]]; then
#         echo "Stopping and disabling the webserver..."
#         sudo systemctl stop chamboard_webserver.service
#         sudo systemctl disable chamboard_webserver.service
#     else
#         echo "Webserver will remain running."
#     fi
# else
#     read -p "Do you want to enable the local webserver to serve static content? (y/n): " ENABLE_WEBSERVER
#     if [[ "$ENABLE_WEBSERVER" =~ ^[Yy]$ ]]; then
#         echo "Creating systemd service for webserver..."
#         sudo bash -c "cat > $WEB_SERVICE_FILE" <<EOF
# [Unit]
# Description=Chamboard Local Webserver
# After=network.target

# [Service]
# ExecStart=python3 -m http.server 8080 --directory $DOCS_DIR
# WorkingDirectory=$DOCS_DIR
# Restart=always
# User=$USER
# Group=$USER

# [Install]
# WantedBy=multi-user.target
# EOF

#         sudo systemctl daemon-reload
#         sudo systemctl enable chamboard_webserver.service
#         sudo systemctl start chamboard_webserver.service
#         echo "Webserver enabled at http://localhost:80"
#     else
#         echo "Webserver setup skipped."
#     fi
# fi

# Webserver Setup
if systemctl is-active --quiet chamboard_webserver.service; then
    echo "The Chamboard webserver is already running."
    read -p "Do you want to keep it running? (y/n): " KEEP_WEBSERVER
    if [[ "$KEEP_WEBSERVER" =~ ^[Nn]$ ]]; then
        echo "Stopping and disabling the webserver..."
        sudo systemctl stop chamboard_webserver.service
        sudo systemctl disable chamboard_webserver.service
    else
        echo "Webserver will remain running."
    fi
else
    read -p "Do you want to enable the local webserver to serve static content and APIs? (y/n): " ENABLE_WEBSERVER
    if [[ "$ENABLE_WEBSERVER" =~ ^[Yy]$ ]]; then
        echo "Creating systemd service for webserver..."
        sudo bash -c "cat > $WEB_SERVICE_FILE" <<EOF
[Unit]
Description=Chamboard Local Webserver with API
After=network.target

[Service]
ExecStart=python3 $PROJECT_DIR/resources/chamboard_webserver.py
WorkingDirectory=$DOCS_DIR
Restart=always
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOF

        sudo systemctl daemon-reload
        sudo systemctl enable chamboard_webserver.service
        sudo systemctl start chamboard_webserver.service
        echo "Webserver enabled at http://localhost:8080"
    else
        echo "Webserver setup skipped."
    fi
fi

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# # Add the cron job
# echo "Setting up cron job to run chamboard.py every 30 minutes..."
# (crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_INTERVAL $HOME/chamboard/venv/bin/python $SCRIPT_PATH >> $CURRENT_LOG 2>&1") | crontab -

# # Add a cron job for log rotation
# echo "Setting up log rotation..."
# LOG_ROTATION_SCRIPT="$LOG_DIR/rotate_logs.sh"
# cat <<EOF > "$LOG_ROTATION_SCRIPT"
# #!/bin/bash

# # Rotate logs if chamboard.log is older than 30 days
# if [ -f "$CURRENT_LOG" ]; then
#     LOG_AGE=\$(find "$CURRENT_LOG" -type f -mtime +30)
#     if [ "\$LOG_AGE" ]; then
#         ARCHIVE_NAME="\$LOG_DIR/chamboard_\$(date +'%Y-%m-%d').log"
#         mv "$CURRENT_LOG" "\$ARCHIVE_NAME"
#         echo "Archived log to \$ARCHIVE_NAME"
#     fi
# fi

# # Cleanup old archived logs
# ARCHIVED_LOGS=\$(ls -t "$LOG_DIR"/chamboard_*.log 2>/dev/null | tail -n +\$((ARCHIVE_RETENTION + 1)))
# if [ "\$ARCHIVED_LOGS" ]; then
#     echo "\$ARCHIVED_LOGS" | xargs rm -f
#     echo "Cleaned up old archived logs."
# fi
# EOF

# chmod +x "$LOG_ROTATION_SCRIPT"

# # Schedule the log rotation script to run daily at midnight
# (crontab -l 2>/dev/null | grep -v "$LOG_ROTATION_SCRIPT"; echo "0 0 * * * $LOG_ROTATION_SCRIPT") | crontab -

# echo "Cron jobs added successfully. You can verify them with 'crontab -l'."
# echo "Logs are located in $LOG_DIR."

# Add the cron job safely
echo "Setting up cron job to run chamboard.py every 30 minutes..."

# Temporary file for the new crontab
TMP_CRON=$(mktemp)

# Safely initialize or overwrite the crontab
crontab -l 2>/dev/null > "$TMP_CRON" || echo "# New crontab initialized" > "$TMP_CRON"

# Remove any existing chamboard.py cron job and append the new one
grep -vF "$SCRIPT_PATH" "$TMP_CRON" > "${TMP_CRON}_new"
echo "$CRON_INTERVAL $HOME/chamboard/venv/bin/python $SCRIPT_PATH >> $CURRENT_LOG 2>&1" >> "${TMP_CRON}_new"

# Install the new crontab
crontab "${TMP_CRON}_new" && echo "Cron job added successfully!"

# Cleanup
rm -f "$TMP_CRON" "${TMP_CRON}_new"

# Verify the new crontab
echo "Final crontab:"
crontab -l

# Create a one-time login message
if [ ! -f "$MOTD_INSTRUCTIONS" ]; then
    echo "Creating one-time setup instructions for next login..."
    sudo mkdir -p /etc/motd.d
    sudo bash -c "cat > $MOTD_INSTRUCTIONS" <<EOF
==================================================================
                        Setup complete!
E-paper display dependencies are installed and SPI is configured.
next steps:
1. Navigate to the project directory: cd $PROJECT_DIR
2. Activate the virtual environment: source $VENV_DIR/bin/activate
3. Run your Playwright script inside the virtual environment.

Recommended: Enable remote access via Tailscale
- For simple and secure remote management, consider setting up Tailscale.
- See README.md for more info.

to cleanup this message...
sudo rm -f $MOTD_INSTRUCTIONS
==================================================================
EOF
    sudo chmod +x $MOTD_INSTRUCTIONS
else
    echo "Setup instructions already created."
fi

# Final message and reboot
echo "Setup complete! Rebooting now..."
sudo reboot
