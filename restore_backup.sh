#!/bin/bash

# Pad naar credentials en logbestanden
STACK_CREDENTIALS="/home/archangel/projects/simple_bot/stack_credentials.json"
LOCAL_BACKUP_DIR="/home/archangel/projects/simple_bot/backups"
REMOTE_BACKUP_DIR="BotLogs/backups"

# Haal credentials op uit stack_credentials.json
SFTP_USERNAME=$(jq -r '.sftp_username' "$STACK_CREDENTIALS")
SFTP_PASSWORD=$(jq -r '.sftp_password' "$STACK_CREDENTIALS")
SFTP_HOST=$(jq -r '.sftp_host' "$STACK_CREDENTIALS")

# Maak lokale back-updirectory aan
mkdir -p "$LOCAL_BACKUP_DIR"

# Lijst back-ups op TransIP STACK
echo "Beschikbare back-ups op TransIP STACK..."
/usr/bin/sshpass -p "$SFTP_PASSWORD" sftp -o "AddressFamily inet" "$SFTP_USERNAME@$SFTP_HOST" << EOF
cd $REMOTE_BACKUP_DIR
ls
bye
EOF

# Vraag gebruiker welke back-up te herstellen
echo "Voer de naam van de back-up in (bijv. simple_bot_backup_2025-04-22_13-00-00.tar.gz):"
read BACKUP_FILE

# Download de back-up
echo "Downloaden van $BACKUP_FILE..."
/usr/bin/sshpass -p "$SFTP_PASSWORD" sftp -o "AddressFamily inet" "$SFTP_USERNAME@$SFTP_HOST" << EOF
cd $REMOTE_BACKUP_DIR
get $BACKUP_FILE $LOCAL_BACKUP_DIR/$BACKUP_FILE
bye
EOF

# Controleer of de download is gelukt
if [ -f "$LOCAL_BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "Back-up succesvol gedownload naar $LOCAL_BACKUP_DIR/$BACKUP_FILE."
else
    echo "Fout: Back-up downloaden mislukt."
    exit 1
fi

# Herstel de back-up
echo "Herstellen van $BACKUP_FILE..."
tar -zxvf "$LOCAL_BACKUP_DIR/$BACKUP_FILE" -C /home/archangel/projects/
echo "Back-up succesvol hersteld."
