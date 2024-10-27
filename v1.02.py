import time
import re
import logging
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText
import argparse

# Configure logging
logging.basicConfig(
    filename='ssh_monitor.log',  # Log file path
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration with command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitor SSH login attempts.')
    parser.add_argument('--logfile', type=str, default='/var/log/auth.log', help='Path to the SSH log file.')
    parser.add_argument('--threshold', type=int, default=5, help='Alert threshold for failed login attempts.')
    parser.add_argument('--check_interval', type=int, default=60, help='Check interval in seconds.')
    parser.add_argument('--email', type=str, required=True, help='Email to send alerts.')
    parser.add_argument('--smtp_server', type=str, required=True, help='SMTP server for sending alerts.')
    parser.add_argument('--smtp_port', type=int, default=587, help='SMTP server port.')
    parser.add_argument('--smtp_user', type=str, required=True, help='SMTP username.')
    parser.add_argument('--smtp_password', type=str, required=True, help='SMTP password.')
    return parser.parse_args()

def send_alert(ip_address, attempts, email_alert, smtp_config):
    subject = f'Alert: Brute Force Attempt Detected'
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

def monitor_ssh(log_file, alert_threshold, check_interval, email_alert, smtp_config):
    attempts = defaultdict(int)
    last_alert_time = defaultdict(int)

    with open(log_file, 'r') as file:
        file.seek(0, 2)  # Move to the end of the file
        logging.info('Starting SSH monitoring...')
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

                if attempts[ip_address] >= alert_threshold:
                    current_time = time.time()
                    if current_time - last_alert_time[ip_address] >= 3600:  # 1 hour cooldown for alerts
                        send_alert(ip_address, attempts[ip_address], email_alert, smtp_config)
                        last_alert_time[ip_address] = current_time  # Update last alert time
                        attempts[ip_address] = 0  # Reset attempts after alerting

if __name__ == '__main__':
    args = parse_arguments()
    smtp_config = {
        'server': args.smtp_server,
        'port': args.smtp_port,
        'user': args.smtp_user,
        'password': args.smtp_password,
    }
    monitor_ssh(args.logfile, args.threshold, args.check_interval, args.email, smtp_config)
