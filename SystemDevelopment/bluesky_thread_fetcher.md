# Bluesky Thread Fetcher Documentation

## 1. Overview

BlueskyThreadFetcher is a Python module designed to fetch threads from Bluesky and save them as structured JSON files. It systematically collects post content, images, playlist, external links, and other information in a reusable format.

## 2. Key Features

- Bluesky authentication
- Thread fetching and parsing
- Content structuring
- JSON file saving
- Comprehensive error handling
- Logging functionality

## 3. Source Code

```python
"""
Module for fetching Bluesky threads and saving them as JSON files.

This module retrieves thread data from Bluesky and saves information such as
post content, images, playlist, and external links as structured JSON data.

Usage Examples:
    from bluesky_thread_fetcher import BlueskyThreadFetcher
    
    # Basic usage
    fetcher = BlueskyThreadFetcher(
        username='your_username',
        password='your_password',
        output_path=Path('output/thread.json')
    )
    fetcher.fetch_and_save_thread('at://example.com/post/123')

    # Using environment variables
    load_dotenv()
    username = os.getenv("BLUESKY_USERNAME")
    password = os.getenv("BLUESKY_PASSWORD")
    
    fetcher = BlueskyThreadFetcher(
        username=username,
        password=password,
        output_path=Path('output/thread.json'),
        log_path=Path('logs/fetch.log')
    )

Dependencies:
    - atproto
    - python-dotenv
    - pathlib
    - logging
    - json
    - typing
"""

from atproto import Client
from atproto.exceptions import AtProtocolError
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import os
import sys
from dotenv import load_dotenv


# Custom exception classes
class BlueskyError(Exception):
    """Base exception class for handling Bluesky-related operations"""
    pass


class AuthenticationError(BlueskyError):
    """Exception class for handling authentication-related operations"""
    pass


class ThreadFetchError(BlueskyError):
    """Exception class for handling thread fetching operations"""
    pass


class FileOperationError(BlueskyError):
    """Exception class for handling file system operations"""
    pass


class ThreadContent:
    """
    Class for holding structured thread content
    
    Attributes:
        text (str): Post text content
        created_at (str): Post timestamp (ISO 8601 format)
        images (List[Dict[str, str]]): List of attached images
        playlist (List[Dict[str, str]]): List of playlist
        external_links (List[Dict[str, str]]): List of external links
    
    Example:
        content = ThreadContent("Post content", "2024-01-01T12:00:00Z")
        content.images.append({"alt": "Image description", "fullsize": "Image URL"})
    """
    def __init__(self, text: str, created_at: str):
        self.text = text
        self.created_at = created_at
        self.images: List[Dict[str, str]] = []
        self.playlist: List[Dict[str, str]] = []
        self.external_links: List[Dict[str, str]] = []

    def to_dict(self) -> Dict:
        """
        Convert ThreadContent object to dictionary format
        
        Returns:
            Dict: Structured thread content dictionary
        """
        content_dict = {
            "text": self.text,
            "datetime": self.created_at
        }
        if self.images:
            content_dict["images"] = self.images
        if self.playlist:
            content_dict["playlist"] = self.playlist
        if self.external_links:
            content_dict["external"] = self.external_links
        return content_dict


class BlueskyThreadFetcher:
    """
    Class for fetching Bluesky threads and saving them in JSON format
    
    Attributes:
        username (str): Bluesky username
        password (str): Bluesky password
        output_path (Path): Output path for JSON file
        logger (logging.Logger): Logging instance
        client (Optional[Client]): atproto client instance
        thread_contents (Dict[str, ThreadContent]): Retrieved thread contents
    """
    
    def __init__(
        self,
        username: str,
        password: str,
        output_path: Path,
        log_path: Optional[Path] = None
    ):
        """
        Initialize BlueskyThreadFetcher
        
        Args:
            username: Bluesky username
            password: Bluesky password
            output_path: Output path for JSON file
            log_path: Path for log file (optional)
            
        Raises:
            ValueError: If required parameters are missing
        """
        if not all([username, password, output_path]):
            raise ValueError("username, password, and output_path are required parameters")
            
        self.username = username
        self.password = password
        self.output_path = Path(output_path)
        self._setup_logging(log_path)
        self.client: Optional[Client] = None
        self.thread_contents: Dict[str, ThreadContent] = {}
        
    def _setup_logging(self, log_path: Optional[Path]) -> None:
        """
        Set up logging configuration
        
        Args:
            log_path: Path for log file (optional)
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console output setup
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File output setup (if specified)
        if log_path:
            try:
                log_path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(
                    log_path,
                    encoding='utf-8'
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.warning(f"Failed to setup logging: {e}")
                
    def _authenticate(self) -> None:
        """
        Authenticate with Bluesky
        
        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            self.client = Client()
            self.client.login(self.username, self.password)
            self.logger.info("Authentication successful")
        except AtProtocolError as e:
            raise AuthenticationError(f"Failed to authenticate: {e}")
            
    def _extract_thread_content(
        self,
        thread: any,
        author_handle: str,
        count: int = 0
    ) -> int:
        """
        Extract content from thread and save as ThreadContent objects
        
        Args:
            thread: Thread object
            author_handle: Author's handle
            count: Post counter
            
        Returns:
            int: Updated counter
        """
        if not hasattr(thread, 'post') or not thread.post:
            return count
            
        post = thread.post
        if not hasattr(post, 'author') or post.author.handle != author_handle:
            return count
            
        if not hasattr(post, 'record') or not post.record.text:
            return count
            
        # Create ThreadContent object
        content = ThreadContent(
            post.record.text,
            post.record.created_at
        )
        
        if hasattr(post, 'embed') and post.embed:
            # Process images
            if hasattr(post.embed, 'images'):
                for img in post.embed.images:
                    content.images.append({
                        "alt": img.alt,
                        "fullsize": img.fullsize
                    })
                    
            # Process playlist
            if hasattr(post.embed, 'playlist'):
                content.playlist.append({
                    "alt": post.embed.alt,
                    "playlist": post.embed.playlist
                })

            # Process external links
            if hasattr(post.embed, 'external'):
                content.external_links.append({
                    "title": post.embed.external.title,
                    "uri": post.embed.external.uri
                })
                
        self.thread_contents[str(count)] = content
        count += 1
        
        # Process replies recursively
        if hasattr(thread, 'replies'):
            for reply in thread.replies:
                count = self._extract_thread_content(
                    reply,
                    author_handle,
                    count
                )
                
        return count
        
    def _save_to_json(self) -> None:
        """
        Save retrieved thread content as JSON file
        
        Raises:
            FileOperationError: If file operation fails
        """
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert ThreadContent objects to dictionary
            output_data = {
                key: content.to_dict()
                for key, content in self.thread_contents.items()
            }
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(
                    output_data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )
            self.logger.info(f"JSON file saved successfully: {self.output_path}")
        except Exception as e:
            raise FileOperationError(f"Failed to save JSON: {e}")
            
    def fetch_and_save_thread(self, thread_uri: str) -> None:
        """
        Fetch thread and save as JSON file
        
        Args:
            thread_uri: URI of thread to fetch
            
        Raises:
            ThreadFetchError: If thread fetching fails
            FileOperationError: If file operation fails
        """
        try:
            self.logger.info(f"Starting thread fetch: {thread_uri}")
            
            # Authenticate
            if not self.client:
                self._authenticate()
                
            # Fetch thread
            thread_data = self.client.get_post_thread(uri=thread_uri)
            
            # Get author's handle
            author_handle = thread_uri.split("//")[1].split("/")[0]
            
            # Extract thread content
            self._extract_thread_content(thread_data.thread, author_handle)
            
            # Save as JSON file
            self._save_to_json()
            
            self.logger.info("Thread fetch and save completed")
            
        except AuthenticationError as e:
            raise ThreadFetchError(f"Failed to authenticate: {e}")
        except AtProtocolError as e:
            raise ThreadFetchError(f"Failed to fetch thread: {e}")
        except FileOperationError as e:
            raise e
        except Exception as e:
            raise ThreadFetchError(f"Failed to process thread: {e}")


def main():
    """
    Main execution function
    
    Environment variables:
        BLUESKY_USERNAME: Bluesky username
        BLUESKY_PASSWORD: Bluesky password
    
    Raises:
        ValueError: If required environment variables are not set
    """
    # Load environment variables
    load_dotenv()
    
    # Get settings from environment variables
    username = os.getenv("BLUESKY_USERNAME")
    password = os.getenv("BLUESKY_PASSWORD")
    
    if not all([username, password]):
        raise ValueError("Environment variables BLUESKY_USERNAME and BLUESKY_PASSWORD are required")
        
    # Set paths
    output_path = Path('output/thread.json')
    log_path = Path('logs/fetch.log')
    
    try:
        # Initialize BlueskyThreadFetcher
        fetcher = BlueskyThreadFetcher(
            username=username,
            password=password,
            output_path=output_path,
            log_path=log_path
        )
        
        # Fetch and save thread
        fetcher.fetch_and_save_thread(
            'at://example.com/app.bsky.feed.post/123abcdefg456'  # Replace with actual thread URI
        )
        
    except (ValueError, BlueskyError) as e:
        logging.error(f"Failed to execute: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Failed to execute: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

## 4. Class Structure

### 1. Custom Exception Classes

```
BlueskyError          # Base exception class
├── AuthenticationError  # Authentication-related errors
├── ThreadFetchError    # Thread fetching errors
└── FileOperationError  # File operation errors
```

### 2. ThreadContent

A class that holds structured content for individual thread posts.

**Attributes**:
- `text`: Post text content
- `created_at`: Post timestamp
- `images`: List of attached images
- `playlist`: List of playlist
- `external_links`: List of external links (link cards)

### 3. BlueskyThreadFetcher

Main class managing thread fetching and saving operations.

**Key Methods**:

1. `__init__`: Initialization
   - Required parameters: username, password, output_path
   - Optional: log_path

2. `_authenticate`: Bluesky authentication
   - Initializes client and performs authentication
   - Raises `AuthenticationError` on failure

3. `_extract_thread_content`: Thread content extraction
   - Parses post content
   - Collects images, playlist and external links
   - Processes replies recursively

4. `_save_to_json`: JSON saving
   - Saves structured data in JSON format
   - Creates directories and writes files

5. `fetch_and_save_thread`: Main execution method
   - Executes complete process from fetching to saving
   - Implements comprehensive error handling

## 5. Usage Examples

### Basic Usage

```python
from bluesky_thread_fetcher import BlueskyThreadFetcher
from pathlib import Path

fetcher = BlueskyThreadFetcher(
    username='your_username',
    password='your_password',
    output_path=Path('output.json'),
    log_path=Path('fetcher.log')
)

fetcher.fetch_and_save_thread('at://example.com/app.bsky.feed.post/123abcdefg456')
```

### Usage with Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("BLUESKY_USERNAME")
password = os.getenv("BLUESKY_PASSWORD")

fetcher = BlueskyThreadFetcher(
    username=username,
    password=password,
    output_path=Path('output.json')
)
```

## 6. Output JSON Format

```json
{
    "0": {
        "text": "Post content 1",
        "datetime": "2024-01-01T12:00:00Z"
    },
    "1": {
        "text": "Post content 2",
        "datetime": "2024-01-01T12:05:00Z",
        "images": [
            {
                "alt": "Image description 1",
                "fullsize": "Image URL"
            },
            {
                "alt": "Image description 2",
                "fullsize": "Image URL"
            }
        ]
    },
    "2": {
        "text": "Post content 3",
        "datetime": "2024-01-01T12:10:00Z",
        "playlist": [
            {
                "alt": "playlist description",
                "playlist": "playlist URL"
            }
        ]
    }
    "3": {
        "text": "Post content 4",
        "datetime": "2024-01-01T12:15:00Z",
        "external": [
            {
                "title": "Link title",
                "uri": "https://example.com"
            }
        ]
    }
}
```

## 7. Error Handling

The script handles the following error conditions:

1. Authentication failures
2. Thread fetching errors
3. File operation errors
4. Missing required parameters

Each error is caught by dedicated exception classes and logged appropriately.

## 8. Logging

Logs are written to two destinations:

1. Console output (always enabled)
2. Log file (when log_path is specified)

Log format:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## 9. Important Notes

1. Password management through environment variables is recommended
2. Be mindful of API rate limits when making multiple requests
3. Parent directories for output paths are created automatically
4. Log file path is optional

## 10. Dependencies

- atproto
- python-dotenv
- pathlib
- logging
- json
- typing

## 11. Troubleshooting

### Common Errors and Solutions

1. AuthenticationError
   - Verify authentication credentials
   - Check network connectivity

2. ThreadFetchError
   - Verify URI format
   - Confirm thread existence
   - Check API rate limits

3. FileOperationError
   - Verify write permissions
   - Check disk space
   - Validate path correctness

---
- Created: 2024-10-28
- Updated: 2024-10-29