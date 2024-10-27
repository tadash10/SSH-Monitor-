
---

### User Manual

# User Manual for SSH Monitoring Script

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
   - [Bash Instructions](#bash-instructions)
   - [PowerShell Instructions](#powershell-instructions)
3. [Usage](#usage)
4. [Integration with Fail2ban](#integration-with-fail2ban)

## Introduction

This SSH monitoring script is designed to detect brute-force login attempts and send email alerts. It logs all activities for future reference and can be integrated with Fail2ban for automatic IP banning.

## Installation

### Bash Instructions

1. **Open Terminal.**

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ssh-monitoring.git
   cd ssh-monitoring

3.Install Python (if not installed):

    For Debian/Ubuntu:

    bash

    sudo apt-get install python3

 4.Run the Script: Ensure you have the necessary permissions to read the log file and execute the script:

bash

    sudo python3 ssh_monitor.py --logfile /var/log/auth.log --threshold 5 --check_interval 60 --email your_email@example.com --smtp_server smtp.example.com --smtp_port 587 --smtp_user your_smtp_user --smtp_password your_smtp_password

PowerShell Instructions

  1. Open PowerShell.

  2.Clone the Repository:

    powershell

        git clone https://github.com/yourusername/ssh-monitoring.git
        cd ssh-monitoring

  3.Install Python (if not installed):

    Download Python from the official website and install it.

  4.Run the Script: Make sure you have the necessary permissions to access the log file:

powershell

    python ssh_monitor.py --logfile "C:\path\to\your\auth.log" --threshold 5 --check_interval 60 --email your_email@example.com --smtp_server smtp.example.com --smtp_port 587 --smtp_user your_smtp_user --smtp_password your_smtp_password

Usage

Refer to the command provided above for both Bash and PowerShell to run the script. Ensure you replace placeholder values with actual details specific to your environment.
Integration with Fail2ban

For enhanced security, follow these steps to integrate with Fail2ban:

    Install Fail2ban:

    bash

sudo apt-get install fail2ban  # For Debian/Ubuntu
sudo yum install fail2ban      # For CentOS/RHEL

Configure Fail2ban: Create or edit /etc/fail2ban/jail.local with the following settings:

ini

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log  # Adjust as needed
maxretry = 5
bantime = 3600

Restart Fail2ban:

bash

sudo systemctl restart fail2ban

Check Status:

bash

sudo fail2ban-client status sshd
