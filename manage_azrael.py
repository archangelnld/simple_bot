#!/usr/bin/env python3
import os
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from .config_manager import ConfigManager

class StackManager:
    def __init__(self):
        self.config = ConfigManager()
        self.setup_logging()
        self.stack_config = self.config.get_setting('stack', {})
        self.setup_rclone_config()

    def setup_logging(self):
        """Setup logging voor de stack operations"""
        log_dir = os.path.join(
            self.config.config['paths']['base_dir'],
            self.config.config['paths']['system_logs']
        )
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'stack_manager.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('StackManager')

    def setup_rclone_config(self):
        """Drop die rclone config voor stack access"""
        try:
            rclone_config = f"""[stack]
type = webdav
url = https://{self.stack_config['server']}
user = {self.stack_config['username']}
pass = {self.stack_config['key']}
vendor = other"""

            config_path = os.path.expanduser('~/.config/rclone/rclone.conf')
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w') as f:
                f.write(rclone_config)
            
            os.chmod(config_path, 0o600)
            self.logger.info("Rclone config is ready to roll")
        except Exception as e:
            self.logger.error(f"Config setup failed: {e}")

    def run_rclone_command(self, command):
        """Execute rclone commands met error handling"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            self.logger.info(f"Command executed: {' '.join(command)}")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {' '.join(command)}, Error: {e.stderr}")
            return False, e.stderr

    def sync_to_stack(self, local_path, remote_path):
        """Push die files naar de cloud"""
        try:
            command = [
                'rclone',
                'sync',
                local_path,
                f"stack:{self.stack_config['base_path']}/{remote_path}",
                '--progress'
            ]
            return self.run_rclone_command(command)
        except Exception as e:
            self.logger.error(f"Sync failed: {e}")
            return False, str(e)

    def sync_from_stack(self, remote_path, local_path):
        """Pull die cloud files terug"""
        try:
            command = [
                'rclone',
                'sync',
                f"stack:{self.stack_config['base_path']}/{remote_path}",
                local_path,
                '--progress'
            ]
            return self.run_rclone_command(command)
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            return False, str(e)

    def list_stack_contents(self, remote_path=""):
        """Check wat er in de cloud staat"""
        try:
            command = [
                'rclone',
                'lsf',
                f"stack:{self.stack_config['base_path']}/{remote_path}"
            ]
            return self.run_rclone_command(command)
        except Exception as e:
            self.logger.error(f"Listing failed: {e}")
            return False, str(e)

    def check_stack_connection(self):
        """Check of we connected zijn met de cloud"""
        try:
            command = [
                'rclone',
                'about',
                'stack:'
            ]
            return self.run_rclone_command(command)
        except Exception as e:
            self.logger.error(f"Connection check failed: {e}")
            return False, str(e)

    def sync_logs_to_stack(self):
        """Auto-sync voor je logs"""
        log_dir = os.path.join(
            self.config.config['paths']['base_dir'],
            self.config.config['paths']['log_dir']
        )
        return self.sync_to_stack(log_dir, 'logs')

    def sync_backups_to_stack(self):
        """Auto-sync voor je backups"""
        backup_dir = os.path.join(
            self.config.config['paths']['base_dir'],
            self.config.config['paths']['backup_dir']
        )
        return self.sync_to_stack(backup_dir, 'backups')

    def get_stack_usage(self):
        """Check hoeveel space je gebruikt"""
        try:
            command = [
                'rclone',
                'about',
                'stack:',
                '--json'
            ]
            success, output = self.run_rclone_command(command)
            if success:
                import json
                usage = json.loads(output)
                return True, usage
            return False, output
        except Exception as e:
            self.logger.error(f"Usage check failed: {e}")
            return False, str(e)

if __name__ == "__main__":
    stack_manager = StackManager()
    success, status = stack_manager.check_stack_connection()
    if success:
        print("Stack connection is live!")
        print(status)
