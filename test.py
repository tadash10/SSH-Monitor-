import time
import re
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText

# Configuration
LOG_FILE = '/var/log/auth.log'  # Path to SSH log file
ALERT_THRESHOLD = 5  # Number of failed attempts before alerting
CHECK_INTERVAL = 60  # Check interval in seconds
EMAIL_ALERT = 'your_email@example.com'  # Email to send alerts
SMTP_SERVER = 'smtp.example.com'  # Your SMTP server
SMTP_PORT = 587  # SMTP port
SMTP_USER = 'your_smtp_user'  # SMTP username
SMTP_PASSWORD = 'your_smtp_password'  # SMTP password

def send_alert(ip_address, attempts):
    subject = f'Alert: Brute Force Attempt Detected'
    body = f'Alert: {attempts} failed SSH login attempts from {ip_address}.'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = EMAIL_ALERT

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, EMAIL_ALERT, msg.as_string())

def monitor_ssh():
    attempts = defaultdict(int)
    with open(LOG_FILE, 'r') as file:
        file.seek(0, 2)  # Move to the end of the file
        while True:
            line = file.readline()
            if not line:
                time.sleep(1)  # Wait for new lines
                continue
            
            # Regex to match failed login attempts
            match = re.search(r'Failed password for invalid user (\S+) from (\S+)', line)
            if match:
                user, ip_address = match.groups()
                attempts[ip_address] += 1
                print(f'Failed login attempt {attempts[ip_address]} from {ip_address}')

                if attempts[ip_address] >= ALERT_THRESHOLD:
                    send_alert(ip_address, attempts[ip_address])
                    attempts[ip_address] = 0  # Reset attempts after alerting

if __name__ == '__main__':
    monitor_ssh()
