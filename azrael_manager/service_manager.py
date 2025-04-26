#!/usr/bin/env python3
import subprocess
import logging
import os
from .config_manager import ConfigManager

class ServiceManager:
    def __init__(self):
        self.config = ConfigManager()
        self.service_name = self.config.get_setting('service', 'name')
        self.setup_logging()

    def setup_logging(self):
        log_dir = os.path.join(
            self.config.config['paths']['base_dir'],
            self.config.config['paths']['system_logs']
        )
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'service_manager.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('ServiceManager')

    def run_command(self, command):
        """Voer een systemctl command uit"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            self.logger.info(f"Command executed successfully: {' '.join(command)}")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {' '.join(command)}, Error: {e.stderr}")
            return False, e.stderr

    def start_service(self):
        """Start de service"""
        return self.run_command(['sudo', 'systemctl', 'start', self.service_name])

    def stop_service(self):
        """Stop de service"""
        return self.run_command(['sudo', 'systemctl', 'stop', self.service_name])

    def restart_service(self):
        """Herstart de service"""
        return self.run_command(['sudo', 'systemctl', 'restart', self.service_name])

    def get_status(self):
        """Haal de service status op"""
        return self.run_command(['sudo', 'systemctl', 'status', self.service_name])

    def enable_service(self):
        """Enable de service om te starten bij boot"""
        return self.run_command(['sudo', 'systemctl', 'enable', self.service_name])

    def disable_service(self):
        """Disable de service bij boot"""
        return self.run_command(['sudo', 'systemctl', 'disable', self.service_name])

    def reload_daemon(self):
        """Reload de systemd daemon"""
        return self.run_command(['sudo', 'systemctl', 'daemon-reload'])

    def update_service_file(self):
        """Update de service configuratie file"""
        service_config = self.config.get_setting('service', None)
        if not service_config:
            self.logger.error("Service configuration not found")
            return False

        service_content = f"""[Unit]
Description={service_config['description']}
After=network.target

[Service]
Type=simple
User={service_config['user']}
Group={service_config['group']}
WorkingDirectory={self.config.config['paths']['base_dir']}
Environment=PYTHONUNBUFFERED=1
Environment=VIRTUAL_ENV=/home/archangel/venv
Environment=PATH=/home/archangel/venv/bin:/usr/local/bin:/usr/bin:/bin

# Resource limieten
MemoryMax={service_config['memory_limit']}
CPUQuota={service_config['cpu_quota']}
LimitNOFILE=65535

# Veiligheid
ProtectSystem=full
PrivateTmp=true
NoNewPrivileges=true

ExecStart=/home/archangel/venv/bin/python3 {self.config.config['paths']['base_dir']}/azrael_bot.py

# Restart policy
Restart=on-failure
RestartSec={service_config['restart_sec']}
StartLimitIntervalSec={service_config['start_limit_interval']}
StartLimitBurst={service_config['start_limit_burst']}

StandardOutput=append:{self.config.config['paths']['base_dir']}/{self.config.config['paths']['system_logs']}/stdout.log
StandardError=append:{self.config.config['paths']['base_dir']}/{self.config.config['paths']['system_logs']}/stderr.log

[Install]
WantedBy=multi-user.target
"""

        try:
            service_path = f"/etc/systemd/system/{self.service_name}.service"
            with open('/tmp/service_file', 'w') as f:
                f.write(service_content)
            
            # Kopieer naar system directory met sudo
            self.run_command(['sudo', 'cp', '/tmp/service_file', service_path])
            self.run_command(['sudo', 'chmod', '644', service_path])
            self.run_command(['sudo', 'chown', 'root:root', service_path])
            
            # Reload daemon
            self.reload_daemon()
            
            self.logger.info("Service file updated successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error updating service file: {e}")
            return False

    def get_logs(self, lines=50):
        """Haal service logs op"""
        return self.run_command(['sudo', 'journalctl', '-u', self.service_name, '-n', str(lines)])

if __name__ == "__main__":
    service_manager = ServiceManager()
    status, output = service_manager.get_status()
    print(output)
