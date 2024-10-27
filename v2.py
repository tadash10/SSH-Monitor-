import time
import re
import logging
import os
import smtplib
from email.mime.text import MIMEText
from collections import defaultdict
import argparse
import json
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='ssh_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration management
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitor SSH login attempts.')
    parser.add_argument('--config', type=str, default='config.json', help='Path to the configuration file.')
    return parser.parse_args()

def send_alert(ip_address, attempts, email_alert, smtp_config):
    subject = 'Alert: Brute Force Attempt Detected'
    body = f'Alert: {attempts} failed SSH login attempts from {ip_address}.'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_config['user']
    msg['To'] = email_alert

    try:
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['user'], smtp_config['password'])
            server.sendmail(smtp_config['user'], email_alert, msg.as_string())
        logging.info(f'Alert sent for IP {ip_address} with {attempts} attempts.')
    except Exception as e:
        logging.error(f'Failed to send alert for IP {ip_address}: {e}')

class LogHandler(FileSystemEventHandler):
    def __init__(self, monitor_function):
        self.monitor_function = monitor_function

    def on_modified(self, event):
        if event.src_path.endswith(args.logfile):
            self.monitor_function()

def monitor_ssh(log_file, alert_threshold, check_interval, email_alert, smtp_config, alert_cooldown):
    attempts = defaultdict(int)
    last_alert_time = defaultdict(int)

    def read_log():
        try:
            with open(log_file, 'r') as file:
                file.seek(0, 2)  # Move to the end of the file
                while True:
                    line = file.readline()
                    if not line:
                        time.sleep(1)  # Wait for new lines
                        continue
                    
                    match = re.search(r'Failed password for .* from (\S+)', line)
                    if match:
                        ip_address = match.group(1)
                        attempts[ip_address] += 1
                        logging.info(f'Failed login attempt {attempts[ip_address]} from {ip_address}')

                        current_time = time.time()
                        if (attempts[ip_address] >= alert_threshold and
                                current_time - last_alert_time[ip_address] >= alert_cooldown):
                            send_alert(ip_address, attempts[ip_address], email_alert, smtp_config)
                            last_alert_time[ip_address] = current_time

        except Exception as e:
            logging.error(f'An error occurred while monitoring: {e}')

    observer = Observer()
    observer.schedule(LogHandler(read_log), path=os.path.dirname(log_file), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    args = parse_arguments()
    config = load_config(args.config)

    smtp_config = {
        'server': os.getenv('SMTP_SERVER', config['smtp_server']),
        'port': config['smtp_port'],
        'user': os.getenv('SMTP_USER', config['smtp_user']),
        'password': os.getenv('SMTP_PASSWORD', config['smtp_password']),
    }
    
    monitor_ssh(
        config['logfile'],
        config['threshold'],
        config['check_interval'],
        config['email'],
        smtp_config,
        config['alert_cooldown']
    )
