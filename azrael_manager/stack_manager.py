#!/usr/bin/env python3
import os
import logging
import shutil
from datetime import datetime
from pathlib import Path
from .config_manager import ConfigManager

class StackManager:
    def __init__(self):
        self.config = ConfigManager()
        self.setup_logging()
        self.stack_config = self.config.get_setting("stack", {})
        self.mount_path = "/home/archangel/STACK"

    def setup_logging(self):
        """Setup logging voor de stack operations"""
        log_dir = os.path.join(
            self.config.config["paths"]["base_dir"],
            self.config.config["paths"]["system_logs"]
        )
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "stack_manager.log")
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger("StackManager")

    def sync_to_stack(self, local_path, remote_path):
        """Push files naar de sshfs-mount"""
        try:
            dest_path = os.path.join(self.mount_path, self.stack_config["base_path"], remote_path)
            os.makedirs(dest_path, exist_ok=True)
            for item in os.listdir(local_path):
                src = os.path.join(local_path, item)
                dst = os.path.join(dest_path, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            self.logger.info(f"Sync successful: {local_path} -> {dest_path}")
            return True, "Sync completed"
        except Exception as e:
            self.logger.error(f"Sync failed: {e}")
            return False, str(e)

    def sync_logs_to_stack(self):
        """Auto-sync voor je logs"""
        log_dir = os.path.join(
            self.config.config["paths"]["base_dir"],
            self.config.config["paths"]["log_dir"]
        )
        return self.sync_to_stack(log_dir, "logs")

    def sync_backups_to_stack(self):
        """Auto-sync voor je backups"""
        backup_dir = os.path.join(
            self.config.config["paths"]["base_dir"],
            self.config.config["paths"]["backup_dir"]
        )
        return self.sync_to_stack(backup_dir, "backups")

    def check_stack_connection(self):
        """Check of de mount actief is"""
        try:
            if os.path.exists(os.path.join(self.mount_path, self.stack_config["base_path"])):
                return True, "Mount is active"
            raise FileNotFoundError("Mount not found")
        except Exception as e:
            self.logger.error(f"Connection check failed: {e}")
            return False, str(e)

if __name__ == "__main__":
    stack_manager = StackManager()
    success, status = stack_manager.check_stack_connection()
    if success:
        print("Stack connection is live!")
        print(status)

