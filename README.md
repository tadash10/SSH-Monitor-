# SSH Monitoring Script

This script monitors SSH login attempts by analyzing the SSH log file. It detects failed login attempts and sends alerts via email when the number of attempts from a specific IP address exceeds a defined threshold. The script uses logging for better traceability and can be integrated with Fail2ban for additional security.

## Features

- Monitors SSH login attempts in real-time.
- Sends email alerts on multiple failed login attempts from the same IP address.
- Logs all activities to a file for review.
- Configurable via command-line arguments.

## Prerequisites

- Python 3.x
- Required Python packages (e.g., `smtplib`, `re`, `argparse`).
- Access to the SSH log file (typically `/var/log/auth.log` or `/var/log/secure`).
- SMTP server details for sending email alerts.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ssh-monitoring.git
   cd ssh-monitoring

    Install Python Dependencies: (No external packages are needed, as this script uses standard libraries.)

Usage

Run the script with the necessary command-line arguments:

python3 ssh_monitor.py --logfile /path/to/your/auth.log --threshold 5 --check_interval 60 --email your_email@example.com --smtp_server smtp.example.com --smtp_port 587 --smtp_user your_smtp_user --smtp_password your_smtp_password

Example Command

python3 ssh_monitor.py --logfile /var/log/auth.log --threshold 5 --check_interval 60 --email alerts@example.com --smtp_server smtp.example.com --smtp_port 587 --smtp_user your_user --smtp_password your_password

Logging

All activity will be logged to ssh_monitor.log. This file will include details of failed login attempts and alert notifications sent.
Integration with Fail2ban

To enhance security, consider integrating this script with Fail2ban. Follow the Fail2ban documentation for installation and configuration instructions.


