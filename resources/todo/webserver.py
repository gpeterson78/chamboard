# Prompt the user to enable the webserver
read -p "Do you want to enable the local webserver to serve static content? (y/n): " ENABLE_WEBSERVER
if [[ "$ENABLE_WEBSERVER" =~ ^[Yy]$ ]]; then
    # Define variables
    STATIC_DIR="$HOME/chamboard/docs"
    WEBSERVER_SCRIPT="$HOME/chamboard/start_webserver.sh"
    PORT=80

    # Ensure the /docs directory exists
    echo "Setting up the static content directory at $STATIC_DIR..."
    mkdir -p "$STATIC_DIR"

    # Move the static content (index.html and any dependencies) to the /docs directory
    if [ -f "$HOME/index.html" ]; then
        mv "$HOME/index.html" "$STATIC_DIR/index.html"
    fi

    # Create a script to start the webserver
    echo "Creating the webserver script at $WEBSERVER_SCRIPT..."
    cat <<EOF > "$WEBSERVER_SCRIPT"
#!/bin/bash
cd "$STATIC_DIR"
echo "Starting webserver to serve static content from $STATIC_DIR on port $PORT..."
python3 -m http.server $PORT
EOF
    chmod +x "$WEBSERVER_SCRIPT"

    # Add a systemd service for the webserver
    echo "Creating systemd service to run the webserver..."
    WEB_SERVICE_FILE="/etc/systemd/system/chamboard_webserver.service"
    sudo bash -c "cat > $WEB_SERVICE_FILE" <<EOF
[Unit]
Description=Chamboard Local Webserver
After=network.target

[Service]
ExecStart=$WEBSERVER_SCRIPT
WorkingDirectory=$STATIC_DIR
Restart=always
User=$USER
Group=$USER

[Install]
WantedBy=multi-user.target
EOF

    # Enable and start the webserver service
    echo "Enabling and starting the webserver service..."
    sudo systemctl daemon-reload
    sudo systemctl enable chamboard_webserver.service
    sudo systemctl start chamboard_webserver.service

    echo "Webserver setup complete. You can access it at http://localhost:$PORT"
else
    echo "Webserver setup skipped."
fi
