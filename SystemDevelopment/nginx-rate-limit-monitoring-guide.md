# Nginx Rate Limit Monitoring

## Introduction
This guide explains the basic methods for monitoring the rate limiting (access restriction) functionality of the Nginx web server.

### Key Terms
- **Nginx**: A high-performance web server software
- **Rate Limiting**: A function that restricts the number of accesses to a server
- **429 Error**: An error returned when a request exceeds the rate limit
- **Log**: Server operation records

## 1. Basic Configuration

Nginx configurations are primarily managed in the following files:
- Main configuration file: `/etc/nginx/nginx.conf`
- Site-specific configurations: `/etc/nginx/conf.d/*.conf` or `/etc/nginx/sites-available/*`

### 1.1 Rate Limit Configuration

**Configuration File Location and Editing Method:**
```bash
# Create a backup of the configuration file (important)
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Edit the configuration file
sudo nano /etc/nginx/nginx.conf
```

**Configuration Content to Add:**
```nginx
# Add the following within the http{} block in /etc/nginx/nginx.conf

# Define rate limit zones
# Here we set up global access limits and API-specific limits
limit_req_zone $binary_remote_addr zone=global:5m rate=3r/s;
limit_req_zone $binary_remote_addr zone=api:5m rate=3r/s;

# Set rate limit log level
limit_req_log_level notice;
```

**Configuration Details:**
- `limit_req_zone`: Directive that defines rate limiting rules
- `$binary_remote_addr`: Uses client IP address as the key
- `zone=global:5m`: 
  - Creates a zone named `global`
  - Allocates 5MB of memory (can store approximately 32,000 IP addresses)
- `rate=3r/s`: Allows up to 3 requests per second

### 1.2 Log Configuration

**Basic Log Configuration:**
```nginx
# Add the following within the http{} block in /etc/nginx/nginx.conf

# Define access log format
log_format monitoring '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    '$request_time '                    # Request processing time
                    '$limit_req_status '               # Rate limit status
                    '$connection '                     # Connection number
                    '$connection_requests '            # Number of requests in current connection
                    'upstream_response_time $upstream_response_time ' # Upstream (backend) response time
                    'upstream_addr $upstream_addr';    # Upstream (backend) address

# Configure log file output
access_log /var/log/nginx/access.log monitoring buffer=32k flush=5s;
error_log /var/log/nginx/error.log notice;

# Output rate limit-specific logs to a separate file (optional)
map $status $loggable {
    429     1;
    default 0;
}

access_log /var/log/nginx/ratelimit.log monitoring if=$loggable buffer=16k flush=5s;
```

### 1.2.1 Log Rotation Configuration

```plaintext
# Create the following configuration in /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily                   # Rotate logs daily
    missingok              # Don't error if log file is missing
    rotate 14              # Keep 14 generations
    compress               # Compress old logs
    delaycompress          # Don't compress the most recently rotated log
    notifempty            # Don't rotate empty log files
    create 0640 nginx adm  # Set permissions and owner for new log files
    sharedscripts         # Run scripts once after all logs are rotated
    postrotate            # Post-rotation script
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 `cat /var/run/nginx.pid`
        fi
    endscript
    
    # Size-based rotation (optional)
    size 100M             # Rotate when size exceeds 100MB
}
```

### 1.2.2 Example Log Output and Variable Explanation

```plaintext
# Normal access log output example
192.168.1.100 - user123 [15/Mar/2024:10:15:30 +0900] "GET /api/users HTTP/1.1" 200 1534 "https://example.com" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 0.002 - 1 3 upstream_response_time 0.001 upstream_addr 10.0.0.10:8080

# Rate limit error log output example
192.168.1.101 - - [15/Mar/2024:10:15:31 +0900] "GET /api/users HTTP/1.1" 429 198 "-" "curl/7.68.0" 0.000 limiting 2 8 upstream_response_time - upstream_addr -

# Variable Explanations
- $remote_addr: "192.168.1.100" - Client IP address
- $remote_user: "user123" - Authenticated username (or "-" if no authentication)
- $time_local: "[15/Mar/2024:10:15:30 +0900]" - Request timestamp
- $request: "GET /api/users HTTP/1.1" - Request line
- $status: "200" or "429" - HTTP status code
- $body_bytes_sent: "1534" - Number of bytes sent in response body
- $http_referer: "https://example.com" - Referer
- $http_user_agent: "Mozilla/5.0..." - User agent
- $request_time: "0.002" - Request processing time (seconds)
- $limit_req_status: "limiting" - Rate limit status (set only when limited)
- $connection: "1" - Connection number
- $connection_requests: "3" - Number of requests in current connection
- $upstream_response_time: "0.001" - Backend response time
- $upstream_addr: "10.0.0.10:8080" - Backend address
```

### 1.2.3 Log Analysis Commands

```bash
# Aggregate rate limit errors by time period
awk '$9 == "429" {print $4}' /var/log/nginx/access.log | cut -d: -f2 | sort | uniq -c

# Check access frequency from specific IPs
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -n 10

# Response time statistics
awk '{print $11}' /var/log/nginx/access.log | sort -n | awk '{count[NR] = $1; sum += $1} END {print "Min:", count[1], "\nMax:", count[NR], "\nAvg:", sum/NR}'
```

### 1.3 Site-Specific Configuration Examples

**Applying rate limits to specific sites or APIs:**
```nginx
# Add to server{} block in /etc/nginx/conf.d/example.conf or
# /etc/nginx/sites-available/example

server {
    listen 80;
    server_name example.com;

    # Global rate limit
    location / {
        limit_req zone=global burst=5 nodelay;
        
        # Other configurations...
    }

    # API-specific rate limit
    location /api/ {
        limit_req zone=api burst=3 nodelay;
        
        # Other API configurations...
    }
}
```

**Configuration Explanation:**
- `burst=5`: Allows bursts of up to 5 requests
- `nodelay`: Process burst requests without delay
- `location /`: Applied to all URLs
- `location /api/`: Applied only to URLs starting with /api/

### 1.4 Configuration Application Procedure

1. **Check Configuration File Syntax**
```bash
# Check for syntax errors in configuration files
sudo nginx -t
```

2. **Reload Nginx**
```bash
# Reload configuration if no errors are found
sudo nginx -s reload
```

### 1.5 Configuration Verification Methods

1. **Verify Rate Limiting**
```bash
# Test by sending multiple requests in a short time
for i in {1..5}; do curl -I http://your-domain.com; done
```

2. **Check Logs**
```bash
# Check access logs
sudo tail -f /var/log/nginx/access.log

# Check error logs
sudo tail -f /var/log/nginx/error.log
```

### 1.6 Troubleshooting

**Common Issues and Solutions:**

1. **Configuration File Not Found**
```bash
# Check Nginx configuration file location
nginx -t
```

2. **Permission Errors**
```bash
# Fix log directory permissions
sudo chmod 755 /var/log/nginx
sudo chown -R nginx:nginx /var/log/nginx
```

3. **Configuration Not Taking Effect**
```bash
# Completely restart Nginx
sudo systemctl restart nginx
```

### 1.7 Security Best Practices

1. **Create Backups**
- Always create backups before configuration changes
- Consider automating regular backups

2. **Set Appropriate Limits**
- Configure rate limits appropriate to your service
- Adjust limits gradually

3. **Configure Monitoring**
- Set up log rotation
- Configure alerts

### 1.8 Important Notes

- Make changes to production environment carefully
- Test configurations in a test environment first
- Always check logs after changes
- Avoid sudden configuration changes, adjust gradually

These configurations set up a basic rate limiting and log monitoring environment. In actual operation, it's important to adjust values according to your service characteristics.

## 2. Basic Monitoring Commands

### 2.1 Real-time Log Monitoring
```bash
# Real-time access log monitoring
tail -f /var/log/nginx/access.log
```
**Usage Points:**
- `-f` option shows latest logs in real-time
- New logs are continuously added to the screen
- Use Ctrl+C to stop monitoring

### 2.2 Collecting Statistics
```bash
# Check number of 429 errors
grep " 429 " /var/log/nginx/access.log | wc -l
```
**Command Explanation:**
- `grep`: Search for specific patterns
- `wc -l`: Count number of lines
- `|`: Pipe output from left command to right command

## 3. Simple Monitoring Script

### 3.1 Basic Monitoring Script
```bash
#!/bin/bash

# Configuration
ACCESS_LOG="/var/log/nginx/access.log"
ERROR_LOG="/var/log/nginx/error.log"
INTERVAL=5  # Monitoring interval (seconds)

# Function: Get timestamp
get_timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# Function: Get number of rate limit errors (429)
get_rate_limit_errors() {
    grep " 429 " "$ACCESS_LOG" | wc -l
}

# Function: Get number of Nginx processes
get_nginx_processes() {
    pgrep nginx | wc -l
}

# Function: Get memory usage (in MB)
get_memory_usage() {
    free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}'
}

# Main processing
while true; do
    clear
    echo "=== Nginx Monitoring Report ===="
    echo "Time: $(get_timestamp)"
    echo "------------------------"
    echo "Rate Limit Errors: $(get_rate_limit_errors)"
    echo "Nginx Processes: $(get_nginx_processes)"
    echo "Memory Usage: $(get_memory_usage)"
    echo "------------------------"
    sleep $INTERVAL
done
```

### 3.2 Usage Instructions

1. **Create and Save Script**
```bash
# Create script
sudo nano /usr/local/bin/nginx_monitor.sh

# Add execution permissions
sudo chmod 744 /usr/local/bin/nginx_monitor.sh
```

2. **Run Script**
```bash
sudo /usr/local/bin/nginx_monitor.sh
```

### 3.3 Script Features
- Clears screen and displays latest information every 5 seconds
- Monitors number of rate limit errors (429)
- Shows number of running Nginx processes
- Displays system memory usage
- Shows information with timestamps

### 3.4 How to Stop Monitoring
- Use `Ctrl+C` to stop monitoring

### 3.5 Customization Examples
- Adjust monitoring interval (change `INTERVAL` value)
- Add display items (e.g., CPU usage)
- Add alert functionality (e.g., email notifications when certain thresholds are exceeded)
- Add log file output functionality

**About Permissions:**
- `744`: Owner can execute, other users can only read
- Use `sudo` for operations requiring root privileges

## 4. Troubleshooting

### 4.1 Common Problems and Solutions

**Steps to check when 429 errors frequently occur:**
1. Check error frequency
2. Identify problematic IP addresses
3. Analyze access patterns
4. Adjust rate limits as needed

### 4.2 Monitoring Points

**Important Monitoring Items:**
- Sudden increase in 429 errors
- Concentrated access from specific IPs
- System resource usage

## 5. Operational Best Practices

### Daily Monitoring Tips
1. Regular Checks
   - Check logs first thing in the morning
   - Early detection of anomalies is important
   
2. Alert Configuration
   - Set up notifications for important errors
   - Configure appropriate thresholds

3. Documentation
   - Record problems and solutions
   - Share information within team

### Important Notes:
- Always use root privileges (sudo) for important commands
- Log file paths may vary by environment
- Always create backups before making changes to production environment
- Handle security settings with care

---
- Created: 2024-11-17
- Updated: 2024-11-17