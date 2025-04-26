#!/usr/bin/env python3
import os
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from .config_manager import ConfigManager

class BackupManager:
    def __init__(self):
        self.config = ConfigManager()
        self.backup_dir = os.path.join(
            self.config.config['paths']['base_dir'],
            self.config.config['paths']['backup_dir']
        )
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)

    def create_backup(self):
        """Maak een backup van het systeem"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'azrael_backup_{timestamp}.tar.gz'
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Directories om te backuppen
            dirs_to_backup = ['config.json', 'data', 'logs']
            
            with tarfile.open(backup_path, 'w:gz') as tar:
                for item in dirs_to_backup:
                    path = os.path.join(self.config.config['paths']['base_dir'], item)
                    if os.path.exists(path):
                        tar.add(path, arcname=item)
            
            return True, f"Backup gemaakt: {backup_name}"
        except Exception as e:
            return False, f"Backup fout: {str(e)}"

    def list_backups(self):
        """Lijst alle beschikbare backups"""
        try:
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.endswith('.tar.gz'):
                    path = os.path.join(self.backup_dir, file)
                    backups.append({
                        'filename': file,
                        'size': os.path.getsize(path),
                        'created': datetime.fromtimestamp(os.path.getctime(path))
                    })
            return True, sorted(backups, key=lambda x: x['created'], reverse=True)
        except Exception as e:
            return False, f"Lijst fout: {str(e)}"

    def restore_backup(self, backup_name):
        """Herstel een backup"""
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if not os.path.exists(backup_path):
                return False, "Backup niet gevonden"
            
            # Maak eerst een backup van huidige staat
            self.create_backup()
            
            # Herstel de backup
            with tarfile.open(backup_path, 'r:gz') as tar:
                tar.extractall(path=self.config.config['paths']['base_dir'])
            
            return True, f"Backup hersteld: {backup_name}"
        except Exception as e:
            return False, f"Herstel fout: {str(e)}"

    def cleanup_old_backups(self, keep_days=7):
        """Verwijder oude backups"""
        try:
            count = 0
            cutoff = datetime.now().timestamp() - (keep_days * 86400)
            
            for file in os.listdir(self.backup_dir):
                if file.endswith('.tar.gz'):
                    path = os.path.join(self.backup_dir, file)
                    if os.path.getctime(path) < cutoff:
                        os.remove(path)
                        count += 1
            
            return True, f"{count} oude backup(s) verwijderd"
        except Exception as e:
            return False, f"Cleanup fout: {str(e)}"
