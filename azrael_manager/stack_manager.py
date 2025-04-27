#!/usr/bin/env python3
import os
import logging
import shutil
from datetime import datetime
from pathlib import Path
import paramiko
from dotenv import load_dotenv

# Laad omgevingsvariabelen uit .env-bestand
load_dotenv()

class StackManager:
    """
    StackManager: Beheert SFTP-verbindingen en uploads naar een stack-opslag.
    
    WAARSCHUWING: Deze module is zorgvuldig geconfigureerd om SFTP-verbindingen te beheren.
    Wijzigingen kunnen leiden tot fouten zoals 'Mount not found' of verbindingsproblemen.
    Pas alleen aan na grondig testen en raadpleeg de documentatie.
    """
    def __init__(self):
        print("Initializing StackManager")
        # Laad inloggegevens uit omgevingsvariabelen
        self.sftp_username = os.getenv("SFTP_USERNAME")
        self.sftp_password = os.getenv("SFTP_PASSWORD")
        self.sftp_host = os.getenv("SFTP_HOST")
        self.base_path = os.getenv("STACK_BASE_PATH", "Azrael3.0")
        self.logs_path = os.getenv("STACK_LOGS_PATH", "Azrael3.0/logs")
        self.backups_path = os.getenv("STACK_BACKUPS_PATH", "Azrael3.0/backups")
        self.keys_path = os.getenv("STACK_KEYS_PATH", "Azrael3.0/keys")
        
        # Valideer essentiële inloggegevens
        if not all([self.sftp_username, self.sftp_password, self.sftp_host]):
            error_msg = "Missing required environment variables: SFTP_USERNAME, SFTP_PASSWORD, SFTP_HOST. Please set these in the .env file."
            print(error_msg)
            raise ValueError(error_msg)
        
        print("Environment variables loaded:", {
            "sftp_username": self.sftp_username,
            "sftp_host": self.sftp_host,
            "base_path": self.base_path,
            "logs_path": self.logs_path,
            "backups_path": self.backups_path,
            "keys_path": self.keys_path
        })
        self.sftp = None
        self.transport = None
        self.setup_logging()
        print("Logging setup complete")

    def setup_logging(self):
        """Configureer logging voor StackManager."""
        log_dir = "logs/bot_logs/system"
        print("Log directory:", log_dir)
        os.makedirs(log_dir, exist_ok=True)
        print("Log directory created if it didn't exist")
        logging.basicConfig(
            filename=os.path.join(log_dir, "stack_manager.log"),
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        self.logger = logging.getLogger(__name__)
        print("Logging configured")

    def connect(self):
        """Maak verbinding met de SFTP-server."""
        try:
            self.transport = paramiko.Transport((self.sftp_host, 22))
            self.transport.connect(username=self.sftp_username, password=self.sftp_password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.logger.info("SFTP connected")
            return True, "SFTP connection successful"
        except Exception as e:
            self.logger.error(f"SFTP connection failed: {e}")
            return False, str(e)

    def close(self):
        """Sluit de SFTP-verbinding."""
        try:
            if self.sftp:
                self.sftp.close()
            if self.transport:
                self.transport.close()
            self.logger.info("SFTP connection closed")
            return True, "SFTP connection closed"
        except Exception as e:
            self.logger.error(f"Failed to close SFTP connection: {e}")
            return False, str(e)

    def check_stack_connection(self):
        """Test de SFTP-verbinding."""
        success, message = self.connect()
        if not success:
            return False, message
        self.close()
        return True, "SFTP connection successful"

    def ensure_stack_directories(self):
        """
        Zorg dat de benodigde mappen bestaan op de SFTP-server.
        WAARSCHUWING: Wijzig deze functie niet zonder de mapstructuur te controleren.
        """
        try:
            for path in [self.base_path, self.logs_path, self.backups_path, self.keys_path]:
                try:
                    self.sftp.stat(path)
                except FileNotFoundError:
                    current_path = ""
                    for part in path.split("/"):
                        if part:
                            current_path = f"{current_path}/{part}" if current_path else part
                            try:
                                self.sftp.stat(current_path)
                            except FileNotFoundError:
                                self.sftp.mkdir(current_path)
                    self.logger.info(f"Created directory: {path}")
            self.logger.info("Stack directories ensured")
            return True, "Directories created successfully"
        except Exception as e:
            self.logger.error(f"Failed to ensure directories: {e}")
            return False, str(e)

    def sync_logs_to_stack(self):
        """Synchroniseer logs naar de stack-opslag."""
        success, message = self.connect()
        if not success:
            return False, message
        try:
            success, message = self.ensure_stack_directories()
            if not success:
                return False, message
            local_log_dir = "logs/bot_logs/system"
            for file in os.listdir(local_log_dir):
                local_path = os.path.join(local_log_dir, file)
                remote_path = os.path.join(self.logs_path, file)
                self.sftp.put(local_path, remote_path)
            self.logger.info("Logs synced to stack")
            return True, "Logs synced successfully"
        except Exception as e:
            self.logger.error(f"Log sync failed: {e}")
            return False, str(e)
        finally:
            self.close()

    def sync_backups_to_stack(self):
        """Synchroniseer backups naar de stack-opslag."""
        success, message = self.connect()
        if not success:
            return False, message
        try:
            success, message = self.ensure_stack_directories()
            if not success:
                return False, message
            local_backup_dir = "backups"
            for file in os.listdir(local_backup_dir):
                local_path = os.path.join(local_backup_dir, file)
                remote_path = os.path.join(self.backups_path, file)
                self.sftp.put(local_path, remote_path)
            self.logger.info("Backups synced to stack")
            return True, "Backups synced successfully"
        except Exception as e:
            self.logger.error(f"Backup sync failed: {e}")
            return False, str(e)
        finally:
            self.close()

    def list_stack_contents(self, directory=None):
        """Lijst de inhoud van een map op de stack-opslag."""
        success, message = self.connect()
        if not success:
            return False, message
        try:
            path = os.path.join(self.base_path, directory) if directory else self.base_path
            files = self.sftp.listdir(path)
            self.logger.info(f"Listed contents of {path}")
            return True, files
        except Exception as e:
            self.logger.error(f"Failed to list contents: {e}")
            return False, str(e)
        finally:
            self.close()

if __name__ == "__main__":
    stack = StackManager()
    stack.sync_backups_to_stack()
