# IP Info CSV Generator

## Overview

This Python script extracts unique IP addresses from Nginx access logs, retrieves detailed information for each IP address using the ipinfo.io API, and outputs the data to a CSV file.

While designed for Nginx, it can be adapted for other web servers like Apache by modifying the regular expression in the `extract_unique_ips` function and adjusting the log file path.

## Main Features

1. Extract unique IP addresses from Nginx access logs
2. Retrieve detailed information for each IP address using the ipinfo.io API
3. Output the collected data to a CSV file

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

1. Download the script to an appropriate location on your server.
2. Install the required library:

```
pip install requests
```

## Configuration

Adjust the following variables in the script to match your environment:

```python
INPUT_FILE = '/var/log/nginx/access.log'
OUTPUT_FILE = '/path/to/your/output/ip_info.csv'
```

## Usage

1. Run the script:

```
python ip_info_csv_generator.py
```

2. The script performs the following steps:
   - Extracts unique IP addresses from the log file
   - Retrieves information for each IP address from the ipinfo.io API
   - Outputs the information to a CSV file

3. Upon completion, a CSV file will be generated at the specified location.

## CSV File Structure

The generated CSV file contains the following columns:

- IP: IP address
- Hostname: Hostname (if available)
- City: City name
- Region: Region name
- Country: Country name
- Org: Organization name (usually ISP)

Example output:

```
ip,hostname,city,region,country,org
192.0.2.1,example1.com,New York,NY,US,AS12345 Example ISP
192.0.2.2,example2.net,London,England,GB,AS67890 Another ISP
192.0.2.3,example3.org,Tokyo,Tokyo,JP,AS11111 Third ISP
192.0.2.4,,Sydney,New South Wales,AU,AS22222 Fourth ISP
192.0.2.5,example5.com,Berlin,Berlin,DE,AS33333 Fifth ISP
```

## Notes

- This script uses the ipinfo.io API. Processing a large number of IP addresses may take time. Be aware of rate limits.
- Without an API key, the script uses the free version of the API. Consider obtaining a paid API key for more requests or additional information.

## Troubleshooting

1. PermissionError: Ensure you have the appropriate permissions to read the access log file.
2. API errors: Check your internet connection and verify that the ipinfo.io API is available.
3. Output errors: Ensure the OUTPUT_FILE path is correct and you have write permissions.

## Customization

- Modify the `get_ip_info` function to use different APIs or information sources if needed.
- To include additional information in the CSV, adjust the `get_ip_info` and `create_csv` functions accordingly.

## Full Script

```python
"""
This script extracts unique IP addresses from a log file, retrieves information
for each IP address using the ipinfo.io API, and outputs the collected data to a CSV file.

Usage:
1. Ensure the required library (requests) is installed.
2. Set the INPUT_FILE and OUTPUT_FILE variables to appropriate paths.
3. Run the script.

Note: This script uses the ipinfo.io API, which may have rate limits.
A 1-second delay between requests is implemented to reduce load.
"""

import re
import csv
import requests
import time
from collections import defaultdict

INPUT_FILE = '/var/log/nginx/access.log'
OUTPUT_FILE = '/path/to/your/output/ip_info.csv'

def extract_unique_ips(file_path):
    """
    Extracts unique IP addresses from a log file.
    
    Args:
    file_path (str): Path to the log file
    
    Returns:
    list: List of unique IP addresses found in the file
    """
    ip_counts = defaultdict(int)
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(ip_pattern, line)
            if match:
                ip = match.group()
                ip_counts[ip] += 1
    return list(ip_counts.keys())

def get_ip_info(ip):
    """
    Retrieves information for an IP address using the ipinfo.io API.
    
    Args:
    ip (str): IP address to look up
    
    Returns:
    dict: Dictionary containing information about the IP address, or None if retrieval fails
    """
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'ip': ip,
            'hostname': data.get('hostname', ''),
            'city': data.get('city', ''),
            'region': data.get('region', ''),
            'country': data.get('country', ''),
            'org': data.get('org', '')
        }
    return None

def create_csv(ips, output_file):
    """
    Outputs IP address information to a CSV file.
    
    Args:
    ips (list): List of IP addresses
    output_file (str): Path to the output CSV file
    """
    fieldnames = ['ip', 'hostname', 'city', 'region', 'country', 'org']
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ip in ips:
            ip_info = get_ip_info(ip)
            if ip_info:
                writer.writerow(ip_info)
            time.sleep(1)  # Reduce load

def main():
    """
    Main function: Extracts unique IP addresses, retrieves information, and outputs to a CSV file.
    """
    print("Extracting unique IP addresses...")
    unique_ips = extract_unique_ips(INPUT_FILE)
    print(f"Found {len(unique_ips)} unique IP addresses.")
    print("Retrieving IP information and creating CSV file...")
    create_csv(unique_ips, OUTPUT_FILE)
    print(f"CSV file '{OUTPUT_FILE}' has been successfully created.")

if __name__ == "__main__":
    main()
```

When using this script, make sure to set the `INPUT_FILE` and `OUTPUT_FILE` values appropriately. Also, ensure that you have the necessary permissions and libraries installed before running the script.

---
- Created: 2024-10-18
- Updated: 2024-10-18