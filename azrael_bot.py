#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import sys
import json
from datetime import datetime
from collections import Counter
import random
import logging
from logging.handlers import RotatingFileHandler
import requests

# Basis configuratie
BASE_DIR = "/home/archangel/projects/simple_bot"
LOG_DIR = os.path.join(BASE_DIR, "logs/bot_logs")
LOG_FILE = os.path.join(LOG_DIR, "azrael_bot.log")
ERROR_LOG = os.path.join(LOG_DIR, "error.log")
CHAT_LOG = os.path.join(LOG_DIR, "new_project_chat_log.txt")
TRIGGER_FILE = os.path.join(BASE_DIR, "trigger_woorden.txt")
URLS_FILE = os.path.join(BASE_DIR, "urls.json")

# Zorg dat log directory bestaat
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuratie
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('Azrael')

class AzraelBot:
    def __init__(self):
        self.last_check_time = 0
        self.check_interval = 300  # 5 minuten
        self.load_trigger_words()
        self.load_urls()

    def load_trigger_words(self):
        """Laad trigger woorden uit bestand"""
        try:
            with open(TRIGGER_FILE, 'r', encoding='utf-8') as f:
                self.trigger_words = set(word.strip().lower() for word in f.readlines())
            logger.info(f"Geladen trigger woorden: {', '.join(self.trigger_words)}")
        except Exception as e:
            logger.error(f"Kon trigger woorden niet laden: {str(e)}")
            self.trigger_words = set()

    def load_urls(self):
        """Laad URLs uit JSON bestand"""
        try:
            with open(URLS_FILE, 'r', encoding='utf-8') as f:
                self.urls = json.load(f)
            logger.info(f"Geladen URLs: {len(self.urls)}")
        except Exception as e:
            logger.error(f"Kon URLs niet laden: {str(e)}")
            self.urls = []

    def check_chat_log(self):
        """Controleer chat log op nieuwe berichten"""
        try:
            if not os.path.exists(CHAT_LOG):
                return

            with open(CHAT_LOG, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            # Check voor trigger woorden
            found_triggers = [word for word in self.trigger_words if word in content]
            if found_triggers:
                logger.info(f"Trigger woorden gevonden: {', '.join(found_triggers)}")
                self.process_triggers(found_triggers)

        except Exception as e:
            logger.error(f"Fout bij checken chat log: {str(e)}")

    def process_triggers(self, triggers):
        """Verwerk gevonden trigger woorden"""
        try:
            # Hier kun je acties toevoegen voor verschillende triggers
            for trigger in triggers:
                if trigger == "dansplaat":
                    logger.info("Dansplaat trigger geactiveerd!")
                    # Voeg hier je dansplaat logica toe
                elif trigger == "leren":
                    logger.info("Leer trigger geactiveerd!")
                    # Voeg hier je leer logica toe

        except Exception as e:
            logger.error(f"Fout bij verwerken triggers: {str(e)}")

    def run(self):
        """Hoofdloop van de bot"""
        logger.info("Azrael bot gestart!")
        
        while True:
            try:
                current_time = time.time()
                
                # Check of het tijd is voor een nieuwe controle
                if current_time - self.last_check_time >= self.check_interval:
                    logger.debug("Start nieuwe controle cyclus")
                    self.check_chat_log()
                    self.last_check_time = current_time
                
                # Voorkom CPU overbelasting
                time.sleep(10)

            except Exception as e:
                logger.error(f"Fout in hoofdloop: {str(e)}")
                time.sleep(30)  # Wacht langer bij fouten

def main():
    bot = AzraelBot()
    bot.run()

if __name__ == "__main__":
    main()
