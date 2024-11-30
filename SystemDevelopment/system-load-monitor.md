# System Load Monitoring and Automatic Service Restart System

## 1. System Overview

This system monitors Linux (Ubuntu) server CPU and memory usage, automatically restarting services when usage exceeds configured thresholds.

## 2. Key Components

### 2.1 Monitoring Script (load-monitor.sh)
Main script that monitors system resources and restarts services as needed.

```bash
#!/bin/bash

# Configuration
MAX_LOAD=80  # CPU threshold (%)
MAX_MEM=90   # Memory threshold (%)
CHECK_INTERVAL=60  # Check interval (seconds)

# Logging
log() {
    logger -t "service-monitor" "$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1"
}

# System load check
check_load() {
    local cpu=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' | cut -d. -f1)
    local mem=$(free | grep Mem | awk '{print ($3/$2) * 100}' | cut -d. -f1)
    
    log "Current load - CPU: ${cpu}%, Memory: ${mem}%"
    
    if [ $cpu -gt $MAX_LOAD ] || [ $mem -gt $MAX_MEM ]; then
        return 0  # Overloaded
    fi
    return 1  # Normal
}

# Service restart
restart_services() {
    log "High load detected. Beginning service restart."
    
    local exclude="systemd.service|systemd-journald.service|sshd.service|network.service"
    
    systemctl list-units --type=service --state=running --no-legend | 
    grep -vE "$exclude" | 
    while read -r unit _; do
        log "Restarting: $unit"
        systemctl restart "$unit"
        sleep 2
    done
    
    log "Service restart completed."
}

# Main process
log "Starting load monitoring"
while true; do
    if check_load; then
        restart_services
        sleep 300  # Wait 5 minutes after restart
    fi
    sleep $CHECK_INTERVAL
done
```

### 2.2 systemd Service Configuration (load-monitor.service)
Configuration file for running the monitoring script as a daemon.

```ini
[Unit]
Description=System Load Monitor and Service Restarter
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/load-monitor.sh
Restart=always
RestartSec=60
User=root

[Install]
WantedBy=multi-user.target
```

## 3. Configuration Parameters

```bash
MAX_LOAD=80     # CPU threshold (%)
MAX_MEM=90      # Memory threshold (%)
CHECK_INTERVAL=60  # Check interval (seconds)
```

## 4. Key Features

### 4.1 System Monitoring
- CPU usage monitoring
- Memory usage monitoring
- Regular status checks (60-second intervals)

### 4.2 Service Restart
- Detection of all running services
- Protection of critical system services
- Sequential restart processing

### 4.3 Logging
- System log recording
- Standard output display
- Timestamped logs

## 5. Installation

1. Create script file
```bash
sudo nano /usr/local/bin/load-monitor.sh
sudo chmod +x /usr/local/bin/load-monitor.sh
```

2. Create service configuration
```bash
sudo nano /etc/systemd/system/load-monitor.service
```

3. Enable service
```bash
sudo systemctl daemon-reload
sudo systemctl enable load-monitor
sudo systemctl start load-monitor
```

## 6. Operation

### 6.1 Check Service Status
```bash
sudo systemctl status load-monitor
```

### 6.2 View Logs
```bash
sudo journalctl -u load-monitor -f
```

### 6.3 Stop Service
```bash
sudo systemctl stop load-monitor
```

## 7. Customization

### 7.1 Excluded Services
Services defined in this variable are excluded from restart:
```bash
exclude="systemd.service|systemd-journald.service|sshd.service|network.service"
```

### 7.2 Threshold Adjustment
Adjust these values according to your environment:
- MAX_LOAD: CPU threshold
- MAX_MEM: Memory threshold
- CHECK_INTERVAL: Check frequency

## 8. Troubleshooting

### 8.1 Service Won't Start
- Check script permissions
- Review logs for detailed errors

### 8.2 Monitoring Issues
- Check system logs
- Verify CPU/memory usage commands

## 9. Precautions

- Test thoroughly before production deployment
- Set appropriate thresholds
- Exclude critical services from restart

## 10. Limitations

- Requires root privileges
- Compatible with systemd systems only
- Depends on specific Linux commands (top, free)

## 11. Security Considerations

- Set appropriate script permissions (runs as root)
- Configure proper log file permissions
- Regular security updates recommended

---
- Created: 2024-11-29
- Updated: 2024-11-29