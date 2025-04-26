#!/bin/bash

# Configuratie
LOG_BASE="/home/archangel/projects/simple_bot/logs"
STACK_CREDS="zgmWEYKgsCfjGVPgk7jYpiQUFqs"
STACK_USER="world2you@world2you.stack.storage"
STACK_SERVER="world2you.stack.storage"
STACK_PATH="Azrael3.0"

# Log directories
mkdir -p "$LOG_BASE"/{bot_logs/{system,learning,interactions,errors},backups}
chmod -R 755 "$LOG_BASE"
chown -R archangel:archangel "$LOG_BASE"

# Log rotatie
find "$LOG_BASE" -type f -name "*.log" -mtime +7 -exec gzip {} \;
find "$LOG_BASE" -type f -name "*.gz" -mtime +30 -delete

# Stack sync
rclone sync "$LOG_BASE" "stack:$STACK_PATH/logs" \
    --user "$STACK_USER" \
    --pass "$STACK_CREDS" \
    --log-file="$LOG_BASE/bot_logs/system/rclone_sync.log"
