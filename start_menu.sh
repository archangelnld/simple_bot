#!/bin/bash
while true; do
    clear
    echo -e "\033[1;34m=== AI Bot & Proxy Start Menu ===\033[0m"
    echo -e "\033[1;33mDatume: 20 april 2025\033[0m"
    echo -e "\033[1;33mLocale: /home/archangel/projects/simple_bot\033[0m"
    echo
    echo "1. Start Squid Proxy"
    echo "2. Start AI Bot (simple_chat.py)"
    echo "3. Controller Squid Status"
    echo "4. Stop oude proxy.py"
    echo "5. Toon logs"
    echo "6. Herstart Squid"
    echo "7. Test AI Bot commando's"
    echo "8. Update AI Bot"
    echo "9. Start AI Bot in achtergrond"
    echo "10. Start Telegram Bot"
    echo "11. Scrape een URL"
    echo "12. Log-menu"
    echo "13. Maak backup"
    echo "14. Toon mapstructuur op TransIP STACK"
    echo "15. Afsluiten"
    echo -e "\033[1;32mKies een nummer tussen 1 en 15:\033[0m"
    read choice

    case $choice in
        1)
            echo "Starten van Squid..."
            sudo systemctl start squid
            echo "Controller systeem status squid"
            sudo systemctl status squid
            read -p "Druk op Enter om verder te gaan..."
            ;;
        2)
            echo "Starten van AI Bot..."
            /home/archangel/projects/simple_bot/start_bot.sh
            read -p "Druk op Enter om terug te keren naar het menu..."
            ;;
        3)
            echo "Controller Squid Status..."
            sudo systemctl status squid
            read -p "Druk op Enter om verder te gaan..."
            ;;
        4)
            echo "Stop oude proxy.py..."
            pkill -f 'python3 proxy.py'
            read -p "Druk op Enter om verder te gaan..."
            ;;
        5)
            echo "Toon logs..."
            cat /home/archangel/projects/simple_bot/logs/bot_logs/chat_log.txt
            read -p "Druk op Enter om verder te gaan..."
            ;;
        6)
            echo "Herstart Squid..."
            sudo systemctl restart squid
            read -p "Druk op Enter om verder te gaan..."
            ;;
        7)
            echo "Test AI Bot commando's..."
            /home/archangel/projects/simple_bot/start_bot.sh
            read -p "Druk op Enter om terug te keren naar het menu..."
            ;;
        8)
            echo "Update AI Bot..."
            cd /home/archangel/projects/simple_bot
            git pull
            read -p "Druk op Enter om verder te gaan..."
            ;;
        9)
            echo "Start AI Bot in achtergrond..."
            /home/archangel/projects/simple_bot/start_bot.sh &
            read -p "Druk op Enter om verder te gaan..."
            ;;
        10)
            echo "Start Telegram Bot..."
            # Voeg hier je Telegram bot startcommando toe
            read -p "Druk op Enter om verder te gaan..."
            ;;
        11)
            echo "Scrape een URL..."
            read -p "Voer de URL in: " url
            /home/archangel/projects/simple_bot/start_bot.sh "scrape url: $url"
            read -p "Druk op Enter om verder te gaan..."
            ;;
        12)
            echo "Log-menu..."
            # Voeg hier je log-menu logica toe
            read -p "Druk op Enter om verder te gaan..."
            ;;
        13)
            echo "Maak backup..."
            /home/archangel/projects/simple_bot/backup.sh
            read -p "Druk op Enter om verder te gaan..."
            ;;
        14)
            echo "Mapstructuur ophalen van TransIP STACK..."
            sshpass -p "PJeB2WHINDBvJalFfaJEE70ZyQI" sftp -oStrictHostKeyChecking=no "world2you@sftp.stack.storage" <<EOF
cd BotLogs
ls
dir
bye
EOF
            read -p "Druk op Enter om verder te gaan..."
            ;;
        15)
            echo "Afsluiten..."
            exit 0
            ;;
        *)
            echo "Ongeldige keuze, probeer een nummer tussen 1 en 15."
            read -p "Druk op Enter om verder te gaan..."
            ;;
    esac
done