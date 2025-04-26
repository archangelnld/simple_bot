#!/usr/bin/env python3
import os
import logging
from datetime import datetime
import gzip
from pathlib import Path
from .config_manager import ConfigManager

class LogManager:
    def __init__(self):
        self.config = ConfigManager()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging voor de LogManager"""
        log_dir = os.path.join(
            self.config.config['paths']['base_dir'],
            self.config.config['paths']['system_logs']
        )
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'log_manager.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('LogManager')

    def get_log_content(self, log_type, lines=50):
        """Haal de inhoud van een log bestand op"""
        try:
            log_path = os.path.join(
                self.config.config['paths']['base_dir'],
                self.config.config['paths'][f'{log_type}_logs'],
                f'{log_type}.log'
            )
            
            if not os.path.exists(log_path):
                return False, "Log file does not exist"
            
            with open(log_path, 'r') as f:
                content = f.readlines()
                return True, content[-lines:]
        except Exception as e:
            self.logger.error(f"Error reading log file: {e}")
            return False, str(e)

    def rotate_logs(self):
        """Voer log rotatie uit"""
        try:
            base_dir = self.config.config['paths']['base_dir']
            log_dir = os.path.join(base_dir, 'logs')
            
            for root, _, files in os.walk(log_dir):
                for file in files:
                    if file.endswith('.log'):
                        file_path = os.path.join(root, file)
                        self._rotate_file(file_path)
            
            return True
        except Exception as e:
            self.logger.error(f"Error during log rotation: {e}")
            return False

    def _rotate_file(self, file_path):
        """Roteer een specifiek log bestand"""
        try:
            if os.path.getsize(file_path) > 1024 * 1024:  # 1MB
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f"{file_path}.{timestamp}.gz"
                
                with open(file_path, 'rb') as f_in:
                    with gzip.open(backup_path, 'wb') as f_out:
                        f_out.write(f_in.read())
                
                # Leeg het originele bestand
                open(file_path, 'w').close()
            return True
        except Exception as e:
            self.logger.error(f"Error rotating file {file_path}: {e}")
            return False

    def cleanup_old_logs(self, days=30):
        """Verwijder oude log bestanden"""
        try:
            base_dir = self.config.config['paths']['base_dir']
            log_dir = os.path.join(base_dir, 'logs')
            current_time = datetime.now().timestamp()
            max_age = days * 24 * 60 * 60
            
            for root, _, files in os.walk(log_dir):
                for file in files:
                    if file.endswith('.gz'):
                        file_path = os.path.join(root, file)
                        if current_time - os.path.getctime(file_path) > max_age:
                            os.remove(file_path)
            return True
        except Exception as e:
            self.logger.error(f"Error cleaning up logs: {e}")
            return False

    def get_log_stats(self):
        """Verzamel statistieken over log bestanden"""
        try:
            stats = {
                'total_files': 0,
                'total_size': 0,
                'oldest_log': None,
                'newest_log': None
            }
            
            base_dir = self.config.config['paths']['base_dir']
            log_dir = os.path.join(base_dir, 'logs')
            
            for root, _, files in os.walk(log_dir):
                for file in files:
                    if file.endswith(('.log', '.gz')):
                        file_path = os.path.join(root, file)
                        stats['total_files'] += 1
                        stats['total_size'] += os.path.getsize(file_path)
            
            return True, stats
        except Exception as e:
            self.logger.error(f"Error getting log stats: {e}")
            return False, str(e)
