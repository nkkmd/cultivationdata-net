# Server Monitoring System using Google Apps Script

## Overview

This system automatically monitors the health of multiple servers using Google Apps Script. It performs health checks every 5 minutes, records results in a spreadsheet, and sends email notifications when issues are detected.

## System Requirements

- Google Account
- Google Apps Script
- Google Spreadsheet

## Source Code

```javascript
// Server health monitoring script
function checkServerHealth() {
  // Set target server URLs
  const servers = [
    { name: 'Server1', url: 'https://example1.com/health' },
    { name: 'Server2', url: 'https://example2.com/health' }
  ];
  
  // Spreadsheet for recording results
  const spreadsheetId = 'YOUR_SPREADSHEET_ID';
  const sheet = SpreadsheetApp.openById(spreadsheetId).getActiveSheet();
  
  // Current timestamp
  const timestamp = new Date();
  
  servers.forEach(server => {
    try {
      // Send HTTP request
      const startTime = new Date().getTime();
      const response = UrlFetchApp.fetch(server.url, {
        muteHttpExceptions: true,
        followRedirects: true,
        validateHttpsCertificates: true,
        timeout: 30
      });
      const endTime = new Date().getTime();
      
      // Calculate response time (milliseconds)
      const responseTime = endTime - startTime;
      
      // Get status code
      const statusCode = response.getResponseCode();
      
      // Determine result
      const status = (statusCode >= 200 && statusCode < 300) ? 'Normal' : 'Error';
      
      // Record in spreadsheet
      sheet.appendRow([
        timestamp,
        server.name,
        status,
        statusCode,
        responseTime + 'ms',
        response.getContentText().slice(0, 100) // First 100 characters of response
      ]);
      
      // Send email notification for errors
      if (status === 'Error') {
        sendAlertEmail(server.name, statusCode, responseTime);
      }
      
    } catch (error) {
      // Error handling
      sheet.appendRow([
        timestamp,
        server.name,
        'Error',
        'N/A',
        'N/A',
        error.toString()
      ]);
      
      sendAlertEmail(server.name, 'Error', null, error.toString());
    }
  });
}

// Function to send alert emails
function sendAlertEmail(serverName, statusCode, responseTime, errorMessage = '') {
  const recipient = 'your-email@example.com';
  const subject = `Server Alert: ${serverName}`;
  
  let body = `
Server Name: ${serverName}
Time: ${new Date().toLocaleString()}
Status: ${statusCode >= 200 && statusCode < 300 ? 'Normal' : 'Error'}
Status Code: ${statusCode}
`;

  if (responseTime) {
    body += `Response Time: ${responseTime}ms\n`;
  }
  
  if (errorMessage) {
    body += `Error Details: ${errorMessage}\n`;
  }
  
  MailApp.sendEmail(recipient, subject, body);
}

// Function to set trigger
function setTrigger() {
  // Delete all existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // Set trigger to run every 5 minutes
  ScriptApp.newTrigger('checkServerHealth')
    .timeBased()
    .everyMinutes(5)
    .create();
}
```

## Setup Instructions

### 1. Prepare Spreadsheet

1. Create new spreadsheet
2. Add following columns:
   - Timestamp
   - Server Name
   - Status
   - Status Code
   - Response Time
   - Response Content

### 2. Script Configuration

1. Open Script Editor from Tools > Script Editor
2. Copy provided code
3. Configure following values for your environment:
   ```javascript
   const spreadsheetId = 'YOUR_SPREADSHEET_ID';
   const servers = [
     { name: 'Server1', url: 'https://example1.com/health' },
     { name: 'Server2', url: 'https://example2.com/health' }
   ];
   const recipient = 'your-email@example.com';
   ```

### 3. Trigger Setup

1. Run `setTrigger()` function
2. Authorize required permissions

## Key Features

### Health Check Function
- Health monitoring via HTTP requests
- Response time measurement
- Status code verification
- Timeout setting (30 seconds)

### Monitoring Result Recording
- Automatic recording to spreadsheet
- Time series data storage
- Detailed error logging

### Alert Notifications
- Email notifications for error detection
- Error detail transmission
- Customizable notification conditions

## Customization Methods

### Changing Monitoring Interval
```javascript
ScriptApp.newTrigger('checkServerHealth')
  .timeBased()
  .everyMinutes(10) // Example: Change to 10-minute interval
  .create();
```

### Adding Monitored Servers
```javascript
const servers = [
  { name: 'Server1', url: 'https://example1.com/health' },
  { name: 'Server2', url: 'https://example2.com/health' },
  { name: 'NewServer', url: 'https://example3.com/health' } // Add new server
];
```

### Customizing Alert Conditions
```javascript
// Example: Set response time threshold
if (responseTime > 5000) { // If over 5 seconds
  sendAlertEmail(server.name, statusCode, responseTime);
}
```

## Troubleshooting

### Common Issues and Solutions

1. Script Not Running
   - Check trigger settings
   - Verify authorization status

2. Email Notifications Not Received
   - Check email address settings
   - Verify Gmail sending limits

3. How to Check Error Logs
   - Check Apps Script execution logs
   - Review error column in spreadsheet

## Security Considerations

- HTTPS certificate validation
- Timeout settings to prevent infinite loops
- Proper error information handling

## Maintenance

### Periodic Inspection Items
- Spreadsheet capacity
- Trigger operation status
- Alert notification appropriateness

### Backup
- Recommend regular spreadsheet backups
- Save script code

## Support and Feedback

For issues or improvement suggestions, please check:
- Google Apps Script documentation
- Spreadsheet sharing settings
- Script execution logs


---
- Created: 2024-12-01
- Updated: 2024-12-01