# Getting Bluesky Posts with '#notice' Tag Using AT Protocol in Python

## 1. Overview

This Python script periodically retrieves posts containing the '#notice' tag from a Bluesky account through the AT Protocol and saves them in JSON format. While this data could also be obtained through RSS, using the AT Protocol allows for the flexibility to add other data as needed.

## 2. Main Features

- Login and feed retrieval from Bluesky account
- Filtering posts with '#notice' tag within a specified date range
- Saving retrieved posts in JSON format
- Error handling and logging
- Periodic execution

## 3. Configuration Parameters

```python
USERNAME = 'cultivationdata.net'  # Bluesky username
PASSWORD = # Password loaded from environment variable
CHECK_INTERVAL = 900  # Check interval (900 seconds = 15 minutes)
NOTICE_COUNT = 50    # Maximum number of notices to retrieve
DAYS_RANGE = 90     # Date range for posts (90 days)
JSON_FILE_PATH = '/var/data/notices/notice.json'  # JSON file save path
```

## 4. Key Functions

### `is_within_date_range()`
- Determines if a post is within the specified date range (within 90 days from now)
- Takes UTC datetime string and returns boolean

### `get_bluesky_client()`
- Initializes Bluesky API client and handles login
- Raises BlueskyNoticeError on login failure

### `save_to_json()`
- Saves retrieved data in JSON format
- Creates destination directory if it doesn't exist

### `bsky_get_notice()`
Main processing function that runs every 15 minutes:
1. Logs into Bluesky
2. Retrieves user posts (up to 50)
3. Filters posts containing #notice tag
4. Extracts posts within 90 days
5. Saves post text, URL, and datetime as JSON

## 5. Error Handling

- Custom exception class `BlueskyNoticeError`
- Handles specific cases like login failures and file operations
- Logs all errors
- Continues processing (retries after 15 minutes) even after errors

## 6. Logging Features

- Records INFO/ERROR level logs
- Outputs to both standard output and file (`/var/log/bluesky/notice.log`)
- Logs major processing status and errors

## 7. Security

- Password loaded from environment variables
- Raises error if environment variable is not set

## 8. Usage

1. Set password in `BLUESKY_PASSWORD` environment variable
2. Run the script
3. Runs continuously until terminated with Ctrl+C

## 9. Dependencies

- atproto: For Bluesky API operations
- python-dotenv: For environment variable loading
- pytz: For timezone handling

## 10. Data Format

JSON structure of saved data:

```json
{
    "0": {
        "text": "Post content",
        "url": "https://bsky.app/profile/username/post/xxxx",
        "datetime": "2024-10-23T08:37:28.402Z"
    },
    ...
}
```

## 11. Full Script

```python
from atproto import Client, IdResolver, models
from atproto.exceptions import AtProtocolError
import json
import time
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/var/log/bluesky/notice.log', encoding='utf-8')
    ]
)

# Load environment variables
load_dotenv()

# Constants
USERNAME = 'cultivationdata.net'
PASSWORD = os.getenv("BLUESKY_PASSWORD")
if not PASSWORD:
    raise ValueError("BLUESKY_PASSWORD environment variable is not set")

CHECK_INTERVAL = 900  # 15 minutes
NOTICE_COUNT = 50    # Number of notices to retrieve
DAYS_RANGE = 90     # How many days of notices to retrieve
JSON_FILE_PATH = Path('/var/data/notices/notice.json')

def is_within_date_range(utc_datetime_str: str) -> bool:
    """
    Determines if a post is within the specified date range.
    Args:
        utc_datetime_str (str): UTC datetime string in "2024-10-23T08:37:28.402Z" format
    Returns:
        bool: True if within date range, False otherwise
    """
    current_date = datetime.now(pytz.UTC).date()
    post_date = datetime.fromisoformat(utc_datetime_str.replace('Z', '+00:00')).date()
    date_threshold = current_date - timedelta(days=DAYS_RANGE)
    return post_date >= date_threshold

class BlueskyNoticeError(Exception):
    """Base exception class for Bluesky notice retrieval"""
    pass

def ensure_directory_exists(file_path: Path) -> None:
    """
    Ensures the directory for the specified file path exists.
    Args:
        file_path (Path): File path to check
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

def get_bluesky_client() -> Client:
    """
    Initializes and logs in to Bluesky API client.
    Returns:
        Client: Logged-in Bluesky API client
    Raises:
        BlueskyNoticeError: On login failure
    """
    try:
        client = Client()
        client.login(USERNAME, PASSWORD)
        return client
    except AtProtocolError as e:
        raise BlueskyNoticeError(f"Failed to login to Bluesky: {str(e)}")

def save_to_json(data: Dict, file_path: Path) -> None:
    """
    Saves data as JSON file.
    Args:
        data (Dict): Data to save
        file_path (Path): Destination file path
    Raises:
        BlueskyNoticeError: On file write failure
    """
    try:
        ensure_directory_exists(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"JSON file saved: {file_path}")
    except IOError as e:
        raise BlueskyNoticeError(f"Failed to write JSON file: {str(e)}")

def bsky_get_notice() -> None:
    """
    Retrieves posts with '#notice' from Bluesky and saves them as JSON file.
    Retries after a set interval if an error occurs.
    """
    while True:
        try:
            client = get_bluesky_client()
            # Get feed
            feed_data = client.get_author_feed(
                actor=USERNAME,
                limit=50  # Get more posts for filtering #notice
            )
            posts = [post.post for post in feed_data.feed]
            notice_json: Dict[str, Dict[str, str]] = {}
            count = 0

            # Extract notice posts
            for post in posts:
                if '#notice' in post.record.text:
                    if not is_within_date_range(post.record.created_at):
                        continue

                    notice_json[str(count)] = {
                        "text": post.record.text,
                        "url": f"https://bsky.app/profile/{USERNAME}/post/{post.uri.split('/')[-1]}",
                        "datetime": post.record.created_at
                    }
                    count += 1
                    logging.info(f"Notice retrieved: {post.record.text[:50]}...")
                    if count == NOTICE_COUNT:
                        break

            # Save JSON file
            save_to_json(notice_json, JSON_FILE_PATH)

        except BlueskyNoticeError as e:
            logging.error(f"Error occurred: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error occurred: {str(e)}")

        logging.info(f"Will check again in {CHECK_INTERVAL} seconds")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    try:
        logging.info("Starting Bluesky notice retrieval script")
        bsky_get_notice()
    except KeyboardInterrupt:
        logging.info("Script terminated")

```

This script provides a robust solution for automatically fetching and storing Bluesky posts with specific tags, which can be useful for creating notice feeds or other automated content aggregation systems.

---
- Created: 2024-10-26
- Updated: 2024-10-26