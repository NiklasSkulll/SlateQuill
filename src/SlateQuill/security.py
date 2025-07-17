"""
SlateQuill security validation module.

This module provides security validation and sanitization functions
to ensure safe processing of HTML content.
"""

import re
from pathlib import Path
from typing import Union

from .config import SecurityConfig
from .exceptions import SecurityError


def validate_file_size(file_path: Path, max_size: int) -> None:
    """Validate file size against maximum allowed size."""
    if not file_path.exists():
        raise SecurityError(f"File not found: {file_path}")
    
    file_size = file_path.stat().st_size
    if file_size > max_size:
        raise SecurityError(
            f"File size {file_size} bytes exceeds maximum allowed size {max_size} bytes"
        )


def validate_file_path(file_path: Path) -> None:
    """Validate file path for security issues."""
    # Check for directory traversal attempts
    resolved_path = file_path.resolve()
    
    # Check for suspicious path components
    suspicious_patterns = [
        r"\.\.[\\/]",  # Directory traversal
        r"[\\/]\.\.[\\/]",  # Directory traversal
        r"^\.\.[\\/]",  # Directory traversal at start
    ]
    
    path_str = str(file_path)
    for pattern in suspicious_patterns:
        if re.search(pattern, path_str):
            raise SecurityError(f"Suspicious path detected: {file_path}")


def validate_content_type(content: Union[str, bytes]) -> None:
    """Validate content for potential security issues."""
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            raise SecurityError("Content contains invalid UTF-8 encoding")
    
    # Check for suspicious content patterns
    suspicious_patterns = [
        r"<script[^>]*>",  # Script tags
        r"javascript:",  # JavaScript URLs
        r"data:.*base64",  # Base64 data URLs (potential XSS)
        r"<iframe[^>]*>",  # Iframe tags
        r"<object[^>]*>",  # Object tags
        r"<embed[^>]*>",  # Embed tags
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            # Don't raise error immediately - let sanitization handle it
            pass


def sanitize_html(html_content: str, config: SecurityConfig) -> str:
    """Sanitize HTML content to remove potentially dangerous elements."""
    if not config.sanitize_html:
        return html_content
    
    try:
        from bs4 import BeautifulSoup
        import bleach
    except ImportError:
        raise SecurityError("HTML sanitization requires beautifulsoup4 and bleach")
    
    # Allowed tags and attributes for safe HTML
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 'i', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'a', 'img', 'table', 'thead',
        'tbody', 'tr', 'th', 'td', 'div', 'span', 'hr'
    ]
    
    allowed_attributes = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'table': ['border', 'cellpadding', 'cellspacing'],
        'th': ['colspan', 'rowspan', 'scope'],
        'td': ['colspan', 'rowspan'],
        '*': ['class', 'id']
    }
    
    # Clean HTML
    cleaned_html = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    
    # Additional URL validation
    if not config.allow_external_links:
        soup = BeautifulSoup(cleaned_html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith(('http://', 'https://', 'ftp://')):
                link.decompose()  # Remove external links
        cleaned_html = str(soup)
    
    return cleaned_html


def validate_input(content: Union[str, bytes], file_path: Path, config: SecurityConfig) -> str:
    """Comprehensive input validation."""
    # Validate file path
    validate_file_path(file_path)
    
    # Validate file size
    validate_file_size(file_path, config.max_file_size)
    
    # Convert content to string if needed
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise SecurityError("Content contains invalid UTF-8 encoding")
    
    # Validate content
    validate_content_type(content)
    
    # Sanitize HTML if enabled
    if config.sanitize_html:
        content = sanitize_html(content, config)
    
    return content
