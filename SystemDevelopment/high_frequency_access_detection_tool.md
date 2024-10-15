# Access Log Monitor: A Customizable High-Frequency Access Detection Tool

## Overview

This script is a tool for monitoring Nginx access logs and detecting high-frequency access patterns. It tracks short-term and long-term high-frequency access for each IP address and sends notifications when configured thresholds are exceeded.
While designed for Nginx, this tool can be adapted for monitoring access to other web servers such as Apache with appropriate modifications. The main areas requiring adjustment are the log file path and the regular expression used to extract IP addresses.

## Features

- Continuous monitoring of Nginx access logs
- Detection of short-term and long-term high-frequency access
- Recording of detected high-frequency access in a CSV file
- Customizable notification function
- Detailed logging functionality

## File Structure

- Script: `/usr/local/bin/nginx_access_monitor.py`
- Configuration file: `/etc/nginx/nginx_access_monitor.conf`
- Output CSV file: `/var/log/nginx/nginx_access_monitor.csv`
- Script log file: `/var/log/nginx/nginx_access_monitor.log`

## Configuration

Contents of the configuration file (`/etc/nginx/nginx_access_monitor.conf`):

```ini
[Settings]
# Nginx access log file
log_file = /var/log/nginx/access.log
# Detect more than 20 accesses in 10 seconds
short_term_threshold = 20
short_term_window = 10
# Detect more than 60 accesses in 1 hour
long_term_threshold = 60
long_term_window = 3600
# Check every 3 seconds
check_interval = 3
```

## Full Script

```python
import re
import time
from collections import defaultdict, deque
import configparser
import sys
import csv
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

# Paths for configuration file, output CSV file, and log file
CONFIG_FILE = '/etc/nginx/nginx_access_monitor.conf'
CSV_FILE = '/var/log/nginx/nginx_access_monitor.csv'
LOG_FILE = '/var/log/nginx/nginx_access_monitor.log'

# Logger configuration
def setup_logger():
    logger = logging.getLogger('NginxAccessMonitor')
    logger.setLevel(logging.INFO)
    # Implement log rotation using RotatingFileHandler
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(logging.INFO)
    # Output to console as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # Set formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

def load_config():
    """
    Load settings from the configuration file.
    Returns:
    dict: A dictionary containing configuration parameters.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    logger.info(f"Loaded configuration file {CONFIG_FILE}")
    return {
        'log_file': config.get('Settings', 'log_file', fallback='/var/log/nginx/access.log'),
        'short_term_threshold': config.getint('Settings', 'short_term_threshold', fallback=20),
        'short_term_window': config.getint('Settings', 'short_term_window', fallback=10),
        'long_term_threshold': config.getint('Settings', 'long_term_threshold', fallback=60),
        'long_term_window': config.getint('Settings', 'long_term_window', fallback=3600),
        'check_interval': config.getint('Settings', 'check_interval', fallback=3)
    }

def parse_log_line(line):
    """
    Parse a log line and extract the IP address.
    Args:
    line (str): The log line to parse.
    Returns:
    str or None: The extracted IP address, or None if not found.
    """
    ip_pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    match = re.match(ip_pattern, line)
    return match.group(1) if match else None

def update_csv(ip, detection_time, frequency, window):
    """
    Update the CSV file, removing old entries for the same IP address and adding the latest information.
    Args:
    ip (str): The detected IP address.
    detection_time (str): The time of detection.
    frequency (int): The detected access frequency.
    window (str): The monitoring time window.
    """
    temp_file = CSV_FILE + '.tmp'
    found = False
    # Create a new CSV file if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['IP', 'Detection Time', 'Frequency', 'Window'])
        logger.info(f"Created new CSV file {CSV_FILE}")
    
    with open(CSV_FILE, 'r', newline='') as csvfile, open(temp_file, 'w', newline='') as tempfile:
        csv_reader = csv.reader(csvfile)
        csv_writer = csv.writer(tempfile)
        # Copy header row
        header = next(csv_reader)
        csv_writer.writerow(header)
        for row in csv_reader:
            if row[0] == ip:
                if not found:
                    csv_writer.writerow([ip, detection_time, frequency, window])
                    found = True
            else:
                csv_writer.writerow(row)
        if not found:
            csv_writer.writerow([ip, detection_time, frequency, window])
    
    os.replace(temp_file, CSV_FILE)
    logger.info(f"Updated CSV file: IP {ip}, Detection Time {detection_time}, Frequency {frequency}, Window {window}")

def write_to_csv(ip, detection_time, frequency, window):
    """
    Record detected high-frequency access to the CSV file.
    Args:
    ip (str): The detected IP address.
    detection_time (str): The time of detection.
    frequency (int): The detected access frequency.
    window (str): The monitoring time window.
    """
    update_csv(ip, detection_time, frequency, window)

def cleanup_ip_counts(ip_counts, current_time, long_term_window):
    """
    Clean up IP count data, removing old entries.
    Args:
    ip_counts (dict): A dictionary containing IP addresses and their access counts.
    current_time (float): The current time (UNIX timestamp).
    long_term_window (int): The long-term monitoring time window (in seconds).
    """
    initial_count = len(ip_counts)
    for ip in list(ip_counts.keys()):
        ip_counts[ip]['short'] = deque([t for t in ip_counts[ip]['short'] if current_time - t <= long_term_window])
        ip_counts[ip]['long'] = deque([t for t in ip_counts[ip]['long'] if current_time - t <= long_term_window])
        if not ip_counts[ip]['short'] and not ip_counts[ip]['long']:
            del ip_counts[ip]
    removed_count = initial_count - len(ip_counts)
    logger.info(f"Performed cleanup of IP count data. Removed {removed_count} entries.")

def check_frequency(ip, counts, current_time, threshold, window, window_type, last_notifications, last_cleanup):
    """
    Check the access frequency for a specified IP address and report if necessary.
    Skip duplicate notifications within a certain time frame.
    Args:
    ip (str): The IP address to check.
    counts (deque): A deque of access timestamps.
    current_time (float): The current time (UNIX timestamp).
    threshold (int): The threshold for considering access as high-frequency.
    window (int): The monitoring time window (in seconds).
    window_type (str): The type of monitoring ("short-term" or "long-term").
    last_notifications (dict): A dictionary storing information about the last notifications.
    last_cleanup (float): The timestamp of the last cleanup (UNIX timestamp).
    Returns:
    tuple: (
        deque: Updated deque of access timestamps,
        dict: Updated dictionary of notification information,
        float: Updated cleanup timestamp
    )
    """
    recent_counts = deque(t for t in counts if current_time - t <= window)
    if len(recent_counts) >= threshold:
        detection_time = datetime.fromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")
        message = f"High-frequency access detected: IP {ip} ({window_type} count: {len(recent_counts)} in the last {window} seconds)"
        # Notification conditions
        notification_key = f"{ip}_{window_type}"
        should_notify = (
            notification_key not in last_notifications or
            current_time - last_notifications[notification_key]['time'] > 3600 or
            last_notifications[notification_key]['count'] * 2 < len(recent_counts)
        )
        if should_notify:
            logger.warning(message)
            print(message)
            write_to_csv(ip, detection_time, len(recent_counts), f"{window}s")
            # Periodic cleanup
            if current_time - last_cleanup > 3600:
                last_notifications = {k: v for k, v in last_notifications.items() if current_time - v['time'] <= 3600}
                last_cleanup = current_time
            # Update the latest access count and time
            last_notifications[notification_key] = {
                'time': current_time,
                'count': len(recent_counts)
            }
        else:
            logger.info(f"Skipped notification (duplicate): {message}")
    return recent_counts, last_notifications, last_cleanup

def get_file_size(filename):
    """Get the file size"""
    try:
        return os.path.getsize(filename)
    except OSError as e:
        logger.error(f"Failed to get file size: {filename}. Error: {e}")
        return 0

def monitor_access_log(config):
    """
    Continuously monitor the Nginx access log and detect high-frequency access.
    Args:
    config (dict): A dictionary containing monitoring settings.
    """
    log_file = config['log_file']
    short_term_threshold = config['short_term_threshold']
    short_term_window = config['short_term_window']
    long_term_threshold = config['long_term_threshold']
    long_term_window = config['long_term_window']
    check_interval = config['check_interval']
    
    logger.info(f"Starting monitoring of Nginx access log: {log_file}")
    logger.info(f"Short-term threshold: {short_term_threshold}, Short-term window: {short_term_window} seconds")
    logger.info(f"Long-term threshold: {long_term_threshold}, Long-term window: {long_term_window} seconds")
    logger.info(f"Check interval: {check_interval} seconds")
    
    # Set appropriate initial maximum length for deques
    ip_counts = defaultdict(lambda: {
        'short': deque(maxlen=100),
        'long': deque(maxlen=1000)
    })
    last_notifications = {}
    last_cleanup = time.time()
    last_size = get_file_size(log_file)
    access_count = 0
    
    while True:
        try:
            current_size = get_file_size(log_file)
            if current_size < last_size:
                logger.warning(f"Log file size decreased. Log rotation may have occurred. Resetting to the beginning of the file.")
                with open(log_file, 'r') as f:
                    f.seek(0, 2)  # Move to the end of the file
                last_size = current_size
            elif current_size > last_size:
                with open(log_file, 'r') as f:
                    f.seek(last_size, 0)  # Start reading from the last position
                    for line in f:
                        current_time = time.time()
                        ip = parse_log_line(line)
                        if ip:
                            ip_counts[ip]['short'].append(current_time)
                            ip_counts[ip]['long'].append(current_time)
                            access_count += 1
                            if access_count % 10 == 0:  # Check frequency every 10 accesses
                                for ip, counts in ip_counts.items():
                                    counts['short'], last_notifications, last_cleanup = check_frequency(ip, counts['short'], current_time, short_term_threshold, short_term_window, "short-term", last_notifications, last_cleanup)
                                    counts['long'], last_notifications, last_cleanup = check_frequency(ip, counts['long'], current_time, long_term_threshold, long_term_window, "long-term", last_notifications, last_cleanup)
                                if current_time - last_cleanup > 3600:  # Cleanup every hour
                                    cleanup_ip_counts(ip_counts, current_time, long_term_window)
                                    last_cleanup = current_time
                last_size = current_size
            logger.info(f"Processed {access_count} accesses")
            time.sleep(check_interval)
        except Exception as e:
            error_message = f"An error occurred: {e}"
            logger.error(error_message, exc_info=True)
            print(error_message)  # Output error notification to standard output
            time.sleep(check_interval)  # Wait for a set time even when an error occurs

if __name__ == "__main__":
    logger.info("Starting Nginx access log monitoring script")
    config = load_config()
    try:
        monitor_access_log(config)
    except KeyboardInterrupt:
        logger.info("Script was manually stopped")
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logger.info("Ending Nginx access log monitoring script")
```

## Key Functions

1. **Log File Monitoring**: The script reads the Nginx access log at configured intervals (default is every 3 seconds) and processes new entries.

2. **Access Frequency Tracking**: It tracks access from each IP address over short-term (default 10 seconds) and long-term (default 1 hour) time windows.

3. **High-Frequency Access Detection**: Generates a warning when access exceeds configured thresholds (default is 20 times in 10 seconds for short-term, and 60 times in 1 hour for long-term).

4. **CSV File Recording**: Detected high-frequency access is recorded in a CSV file. Old records for the same IP address are updated.

5. **Notification Function**: Notifications are generated when high-frequency access is detected. By default, it uses the print function to output to the console, but this can be customized according to user requirements.

   Note: For actual use, it's recommended to implement a notification method suitable for your environment, such as email sending, Slack notifications, or writing to system logs.

6. **Log Rotation Handling**: The script automatically starts monitoring the new log file if the Nginx log file is rotated.

## Usage

1. Ensure the configuration file (`/etc/nginx/nginx_access_monitor.conf`) is properly set up.
2. Verify that the required Python package (configparser) is installed.
3. Run the script: `python /usr/local/bin/nginx_access_monitor.py`

For continuous monitoring, it's recommended to set up this script as a systemd service.

## Logging

- Log levels: INFO (normal operation), WARNING (high-frequency access detection), ERROR (error situations)
- Log rotation: Automatic rotation every 10MB, keeping a maximum of 5 old log files

## Precautions

- Monitor system resource usage and adjust settings as necessary.
- Be mindful of memory usage in environments with high traffic volumes.

## Troubleshooting

If errors occur, detailed information is recorded in the log file (`/var/log/nginx/nginx_access_monitor.log`). Check the log file to identify the cause of the error.

## Security

- Set appropriate access permissions for the script and log files.
- Adjust the high-frequency access detection thresholds to suit your environment.

## Customization

- Various parts of the script, such as notification methods and log formats, can be customized to fit specific environments or needs. Modify the code as needed and conduct testing.

---
- Created: 2024-10-15
- Updated: 2024-10-15