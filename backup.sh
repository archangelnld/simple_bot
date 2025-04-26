#!/bin/bash
BACKUP_DIR="simple_bot_$(date +%Y%m%d_%H%M%S)"
TEMP_DIR="/home/archangel/backup/$BACKUP_DIR"
mkdir -p "$TEMP_DIR"
rsync -a --exclude='logs/*' --exclude='venv/*' --exclude='*.tar.gz' /home/archangel/projects/simple_bot/ "$TEMP_DIR/"
tar -czf "$TEMP_DIR.tar.gz" -C "$TEMP_DIR" .
# Upload naar TransIP STACK via SFTP naar BotLogs/backups
sshpass -p "PJeB2WHINDBvJalFfaJEE70ZyQI" sftp -oStrictHostKeyChecking=no "world2you@sftp.stack.storage" <<EOF
mkdir BotLogs
mkdir BotLogs/backups
put $TEMP_DIR.tar.gz BotLogs/backups/$BACKUP_DIR.tar.gz
bye
EOF
rm -rf "$TEMP_DIR" "$TEMP_DIR.tar.gz"
find /home/archangel/backup -name "simple_bot_*.tar.gz" -mtime +7 -delete
echo "Backup geüpload naar TransIP STACK: BotLogs/backups/$BACKUP_DIR.tar.gz"