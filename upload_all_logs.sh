#!/bin/bash

# Pad naar credentials en logbestanden
STACK_CREDENTIALS="/home/archangel/projects/simple_bot/stack_credentials.json"
CHAT_LOG="/home/archangel/projects/simple_bot/logs/bot_logs/chat_log.txt"
CHAT_HISTORY_LOG="/home/archangel/projects/simple_bot/logs/scrape_logs/chat_history.txt"
WGET_LOG_DIR="/home/archangel/projects/simple_bot/logs/wget_logs"
TIMESTAMP=$(date +%F_%H-%M-%S)
TEMP_LOG_DIR="/tmp/system_logs_${TIMESTAMP}"
REMOTE_LOG_DIR="/Azrael3.0/logs"

# Controleer of credentials bestand bestaat
if [[ ! -f "$STACK_CREDENTIALS" ]]; then
    echo "Fout: stack_credentials.json niet gevonden op $STACK_CREDENTIALS"
    exit 1
fi

# Haal credentials op uit stack_credentials.json
SFTP_USERNAME=$(jq -r '.sftp_username' "$STACK_CREDENTIALS")
SFTP_PASSWORD=$(jq -r '.sftp_password' "$STACK_CREDENTIALS")
SFTP_HOST=$(jq -r '.sftp_host' "$STACK_CREDENTIALS")

# Controleer of credentials niet leeg zijn
if [[ -z "$SFTP_USERNAME" || -z "$SFTP_PASSWORD" || -z "$SFTP_HOST" ]]; then
    echo "Fout: Een of meer SFTP-credentials zijn leeg"
    exit 1
fi

# Maak een tijdelijke directory voor logs
mkdir -p "$TEMP_LOG_DIR/systemd" "$TEMP_LOG_DIR/squid" "$TEMP_LOG_DIR/wget"

# Verzamel logs
echo "=== Squid Status ===" > "$TEMP_LOG_DIR/systemd/squid_status_${TIMESTAMP}.txt"
systemctl status squid >> "$TEMP_LOG_DIR/systemd/squid_status_${TIMESTAMP}.txt" 2>/dev/null || echo "Squid service niet actief" >> "$TEMP_LOG_DIR/systemd/squid_status_${TIMESTAMP}.txt"

echo "=== Simple Chat Service Status ===" > "$TEMP_LOG_DIR/systemd/simple_chat_status_${TIMESTAMP}.txt"
systemctl status simple_chat.service >> "$TEMP_LOG_DIR/systemd/simple_chat_status_${TIMESTAMP}.txt" 2>/dev/null || echo "Simple chat service niet actief" >> "$TEMP_LOG_DIR/systemd/simple_chat_status_${TIMESTAMP}.txt"

echo "=== Squid Access Log ===" > "$TEMP_LOG_DIR/squid/squid_access_log_${TIMESTAMP}.txt"
tail -n 100 /var/log/squid/access.log >> "$TEMP_LOG_DIR/squid/squid_access_log_${TIMESTAMP}.txt" 2>/dev/null || echo "Geen access log beschikbaar" >> "$TEMP_LOG_DIR/squid/squid_access_log_${TIMESTAMP}.txt"

echo "=== Squid Cache Log ===" > "$TEMP_LOG_DIR/squid/squid_cache_log_${TIMESTAMP}.txt"
tail -n 100 /var/log/squid/cache.log >> "$TEMP_LOG_DIR/squid/squid_cache_log_${TIMESTAMP}.txt" 2>/dev/null || echo "Geen cache log beschikbaar" >> "$TEMP_LOG_DIR/squid/squid_cache_log_${TIMESTAMP}.txt"

echo "=== Chat Log ===" > "$TEMP_LOG_DIR/chat_log_${TIMESTAMP}.txt"
cat "$CHAT_LOG" >> "$TEMP_LOG_DIR/chat_log_${TIMESTAMP}.txt" 2>/dev/null || echo "Geen chat log beschikbaar" >> "$TEMP_LOG_DIR/chat_log_${TIMESTAMP}.txt"

echo "=== Chat History Log ===" > "$TEMP_LOG_DIR/chat_history_log_${TIMESTAMP}.txt"
cat "$CHAT_HISTORY_LOG" >> "$TEMP_LOG_DIR/chat_history_log_${TIMESTAMP}.txt" 2>/dev/null || echo "Geen chat history log beschikbaar" >> "$TEMP_LOG_DIR/chat_history_log_${TIMESTAMP}.txt"

# Kopieer wget-logs
cp -r "$WGET_LOG_DIR"/* "$TEMP_LOG_DIR/wget/" 2>/dev/null || echo "Geen wget logs beschikbaar" >> "$TEMP_LOG_DIR/wget_logs.txt"

# Controleer en maak submappen op TransIP STACK
SUBDIRS=("systemd" "squid" "wget")
for SUBDIR in "${SUBDIRS[@]}"; do
    /usr/bin/sshpass -p "$SFTP_PASSWORD" sftp -o "AddressFamily inet" "$SFTP_USERNAME@$SFTP_HOST" > /tmp/sftp_output.txt 2>&1 <<EOF
cd $REMOTE_LOG_DIR
ls dir $SUBDIR
bye
EOF
    if ! grep -q "dir.*$SUBDIR" /tmp/sftp_output.txt 2>/dev/null; then
        /usr/bin/sshpass -p "$SFTP_PASSWORD" sftp -o "AddressFamily inet" "$SFTP_USERNAME@$SFTP_HOST" <<EOF
cd $REMOTE_LOG_DIR
mkdir $SUBDIR
bye
EOF
    fi
done

# Upload logs naar de juiste submappen
for SUBDIR in "${SUBDIRS[@]}"; do
    /usr/bin/sshpass -p "$SFTP_PASSWORD" sftp -o "AddressFamily inet" "$SFTP_USERNAME@$SFTP_HOST" <<EOF
cd $REMOTE_LOG_DIR/$SUBDIR
put $TEMP_LOG_DIR/$SUBDIR/*
bye
EOF
done

# Upload chatlogs naar root log directory
/usr/bin/sshpass -p "$SFTP_PASSWORD" sftp -o "AddressFamily inet" "$SFTP_USERNAME@$SFTP_HOST" <<EOF
cd $REMOTE_LOG_DIR
put $TEMP_LOG_DIR/chat_log_${TIMESTAMP}.txt
put $TEMP_LOG_DIR/chat_history_log_${TIMESTAMP}.txt
bye
EOF

# Schoon tijdelijke bestanden op
rm -rf "$TEMP_LOG_DIR" /tmp/sftp_output.txt 2>/dev/null

echo "Logs succesvol geüpload naar TransIP STACK in $REMOTE_LOG_DIR"