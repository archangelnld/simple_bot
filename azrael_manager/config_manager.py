#!/usr/bin/env python3
import json
import os
import logging
from pathlib import Path
import shutil
from datetime import datetime

class ConfigManager:
    def __init__(self, config_path="/home/archangel/projects/simple_bot/config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.setup_logging()
        self.ensure_directories()

    def load_config(self):
        """Laad de configuratie uit het JSON bestand"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return self.create_default_config()

    def create_default_config(self):
        """Maak een standaard configuratie als er geen bestaat"""
        default_config = {
            "urls": {
                "chat_urls": [
                    "https://chat.openai.com",
                    "https://claude.ai",
                    "https://bard.google.com"
                ],
                "learning_urls": [
                    "https://raw.githubusercontent.com/OpenTaal/opentaal-wordlist/master/words.txt",
                    "https://raw.githubusercontent.com/OpenTaal/opentaal-wordlist/master/basiswoorden-gekeurd.txt"
                ],
                "backup_urls": [
                    "https://world2you.stack.storage",
                    "https://drive.example.com/backup"
                ]
            },
            "stack": {
                "username": "world2you@world2you.stack.storage",
                "key": "zgmWEYKgsCfjGVPgk7jYpiQUFqs",
                "server": "world2you.stack.storage",
                "base_path": "Azrael3.0"
            },
            "paths": {
                "base_dir": "/home/archangel/projects/simple_bot",
                "log_dir": "logs/bot_logs",
                "data_dir": "data",
                "backup_dir": "backups",
                "system_logs": "logs/bot_logs/system",
                "learning_logs": "logs/bot_logs/learning",
                "interaction_logs": "logs/bot_logs/interactions",
                "error_logs": "logs/bot_logs/errors"
            },
            "settings": {
                "check_interval": 300,
                "max_retries": 3,
                "log_rotation_size": 1048576,
                "log_backup_count": 5,
                "scrape_cooldown": 3600,
                "editor": {
                    "default": "nano",
                    "mobaxterm_enabled": True,
                    "mobaxterm_path": "/usr/bin/mcedit",
                    "fallback": "nano"
                }
            },
            "service": {
                "name": "azrael-learn",
                "description": "Azrael Continuous Learning Service",
                "user": "archangel",
                "group": "archangel",
                "memory_limit": "1G",
                "cpu_quota": "200%",
                "restart_sec": 30,
                "start_limit_interval": 300,
                "start_limit_burst": 3
            },
            "logging": {
                "rotation_interval": "1d",
                "max_size": "100M",
                "compression": True,
                "retention_days": 30,
                "sync_interval": 14400
            }
        }
        self.save_config(default_config)
        return default_config

    def save_config(self, config=None):
        """Sla de configuratie op naar het JSON bestand"""
        if config is None:
            config = self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            return False

    def setup_logging(self):
        """Configureer logging"""
        try:
            log_dir = os.path.join(
                self.config['paths']['base_dir'],
                self.config['paths']['system_logs']
            )
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, 'config_manager.log')
            
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        except Exception as e:
            print(f"Error setting up logging: {e}")

    def ensure_directories(self):
        """Zorg dat alle benodigde directories bestaan"""
        try:
            for key, path in self.config['paths'].items():
                full_path = os.path.join(self.config['paths']['base_dir'], path)
                Path(full_path).mkdir(parents=True, exist_ok=True)
                logging.info(f"Ensured directory exists: {full_path}")
        except Exception as e:
            logging.error(f"Error creating directories: {e}")

    def get_setting(self, section, default=None):
        """Haal een sectie op uit de config"""
        return self.config.get(section, default)

    def update_setting(self, section, key, value):
        """Update een specifieke instelling"""
        try:
            if section in self.config:
                self.config[section][key] = value
                self.save_config()
                logging.info(f"Updated setting {section}.{key} to {value}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error updating setting: {e}")
            return False

    def backup_config(self):
        """Maak een backup van de configuratie"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(
                self.config['paths']['base_dir'],
                self.config['paths']['backup_dir']
            )
            backup_file = f'config_{timestamp}.json.backup'
            backup_path = os.path.join(backup_dir, backup_file)
            
            os.makedirs(backup_dir, exist_ok=True)
            shutil.copy2(self.config_path, backup_path)
            
            logging.info(f"Created config backup at {backup_path}")
            return True, backup_path
        except Exception as e:
            logging.error(f"Error creating config backup: {e}")
            return False, str(e)

if __name__ == "__main__":
    config = ConfigManager()
    print("Configuration loaded successfully")
