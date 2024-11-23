# Useful Linux Commands Reference Guide

A collection of useful commands for various Linux distributions (Ubuntu, Fedora, CentOS, etc.). Each command includes a brief explanation. For detailed information, please refer to the respective man pages.

Note: Some commands may depend on specific distributions or package managers. In such cases, please use the appropriate commands for your system.

## Table of Contents

1. System Information
2. Process Management
3. System Monitoring
4. Network
5. File System
6. System Logs
7. Package Management
8. System Resource Management
9. File Operations
10. Network Diagnostics
11. System Administration
12. Performance Analysis
13. Security
14. Backup and Compression

## 1. System Information

### Check Memory Usage
Display current memory usage as a percentage:
```bash
free | grep Mem | awk '{print "Memory Usage: " ($3/$2) * 100.0 "%"}'
```
Note: Simple checks can also be done with `free -m` or `free -h`

### Check Storage Usage
Display storage usage percentage for root directory (/):
```bash
df -h / | awk 'NR==2 {print "Storage Usage: " $5}'
```

## 2. Process Management

### Display Running Programs (Processes)
Show detailed information for all running processes:
```bash
ps aux
```

### Display Process Tree Structure
Visualize parent-child relationships of processes in tree structure:
```bash
pstree
```

### Interactive Process Viewer
Real-time system activity monitoring tool:
```bash
top
```

### Display Resource-Intensive Processes
Show top 5 processes by CPU usage:
```bash
ps aux --sort=-%cpu | head -n 5
```

## 3. System Monitoring

### Check System Load
Display system uptime, number of users, and load averages:
```bash
uptime
```

### Monitor Disk I/O
Display disk I/O statistics every second:
```bash
iostat -x 1
```
Note: iostat is part of the sysstat package. To install on Debian-based systems:
```bash
sudo apt install sysstat
```

## 4. Network

### Display Network Connections
Show active TCP/UDP connections and listening ports:
```bash
ss -tuln
```
Note: ss is recommended as a replacement for netstat

### Check IP Address
Display network interfaces and IP addresses:
```bash
ip addr show
```

## 5. File System

### Check Directory Size
Display total size of specified directory in human-readable format:
```bash
du -sh /path/to/directory
```

### Find Large Files
Search for files larger than 100MB from root directory:
```bash
find / -type f -size +100M
```

## 6. System Logs

### Display System Logs
Show last 50 lines of system logs:
```bash
journalctl -n 50
```

## 7. Package Management

### List Installed Packages (Debian-based)
Display all installed packages:
```bash
dpkg -l
```

### List Installed Packages (RPM-based)
Display all installed packages on RPM-based systems:
```bash
rpm -qa
```

## 8. System Resource Management

### Display CPU Information
Show detailed CPU information including architecture, cores, and threads:
```bash
lscpu
```

### List Running Services
Display list of currently running system services:
```bash
systemctl list-units --type=service
```

## 9. File Operations

### Search String in File
Search for specific string in specified file:
```bash
grep "search_string" /path/to/file
```

### Compare Files
Compare two files and display differences in unified format:
```bash
diff -u file1 file2
```

## 10. Network Diagnostics

### Port Scanning
Scan open ports on localhost (can also be used for remote hosts):
```bash
nmap localhost
```
Note: To install nmap:
- Debian-based: `sudo apt install nmap`
- RPM-based: `sudo dnf install nmap`

### DNS Lookup
Display detailed DNS information for specified domain:
```bash
dig example.com
```

## 11. System Administration

### Display Command History
Show recently used commands:
```bash
history
```

### Schedule System Restart
Schedule system restart in 60 minutes:
```bash
shutdown -r +60
```

## 12. Performance Analysis

### Trace System Calls
Track system calls and signals for specified command:
```bash
strace command
```

### Process Resource Usage
Measure execution time and resource usage of specified command:
```bash
time command
```

## 13. Security

### Change File Permissions
Modify file permissions (example gives read-write to owner, read-only to group and others):
```bash
chmod 644 file
```

### Change File Ownership
Change file owner and group:
```bash
chown user:group file
```

## 14. Backup and Compression

### Compress Directory
Compress specified directory in tar.gz format:
```bash
tar -czvf archive.tar.gz /path/to/directory
```

### Extract Files
Extract ZIP file:
```bash
unzip file.zip
```