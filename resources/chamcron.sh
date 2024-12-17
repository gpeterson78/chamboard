#!/bin/bash

# script to setup the cronjobs needed for automatic refresh
# for testing and development purposes

# Exit on any error
set -e

# Customizable Variables
CRON_INTERVAL="*/30 * * * *"  # Every 30 minutes
SCRIPT_PATH="$HOME/chamboard/chamboard.py"  # Full path to chamboard.py
LOG_DIR="$HOME/chamboard/logs"  # Directory to store logs
CURRENT_LOG="$LOG_DIR/chamboard.log"  # Current log file
ARCHIVE_RETENTION=3  # Number of archived logs to retain

# Ensure the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "ERROR: chamboard.py not found at $SCRIPT_PATH"
    exit 1
fi

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Add the cron job
echo "Setting up cron job to run chamboard.py every 30 minutes..."
(crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_INTERVAL $HOME/chamboard/venv/bin/python $SCRIPT_PATH >> $CURRENT_LOG 2>&1") | crontab -

# Add a cron job for log rotation
echo "Setting up log rotation..."
LOG_ROTATION_SCRIPT="$LOG_DIR/rotate_logs.sh"
cat <<EOF > "$LOG_ROTATION_SCRIPT"
#!/bin/bash

# Rotate logs if chamboard.log is older than 30 days
if [ -f "$CURRENT_LOG" ]; then
    LOG_AGE=\$(find "$CURRENT_LOG" -type f -mtime +30)
    if [ "\$LOG_AGE" ]; then
        ARCHIVE_NAME="\$LOG_DIR/chamboard_\$(date +'%Y-%m-%d').log"
        mv "$CURRENT_LOG" "\$ARCHIVE_NAME"
        echo "Archived log to \$ARCHIVE_NAME"
    fi
fi

# Cleanup old archived logs
ARCHIVED_LOGS=\$(ls -t "$LOG_DIR"/chamboard_*.log 2>/dev/null | tail -n +\$((ARCHIVE_RETENTION + 1)))
if [ "\$ARCHIVED_LOGS" ]; then
    echo "\$ARCHIVED_LOGS" | xargs rm -f
    echo "Cleaned up old archived logs."
fi
EOF

chmod +x "$LOG_ROTATION_SCRIPT"

# Schedule the log rotation script to run daily at midnight
(crontab -l 2>/dev/null | grep -v "$LOG_ROTATION_SCRIPT"; echo "0 0 * * * $LOG_ROTATION_SCRIPT") | crontab -

echo "Cron jobs added successfully. You can verify them with 'crontab -l'."
echo "Logs are located in $LOG_DIR."
